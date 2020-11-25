import aiger_bv as BV
import aiger_discrete
from aiger_bv import atom, ite, split_gate, encode_int, lookup
from bidict import bidict

import aiger_gridworld as G


NORTH = '↑'
SOUTH = '↓'
EAST = '→'
WEST = '←'


ACTIONS = bidict({
    #      y   x
    '←': 0b00_01,
    '→': 0b00_10,
    '↓': 0b01_00,
    '↑': 0b10_00,
})


ACTIONS_C = bidict({'←': 0b00, '↑': 0b01, '→': 0b10, '↓': 0b11})
COMPRESSION_MAPPING = {
    ACTIONS_C['→']: ACTIONS['→'],
    ACTIONS_C['←']: ACTIONS['←'],
    ACTIONS_C['↑']: ACTIONS['↑'],
    ACTIONS_C['↓']: ACTIONS['↓'],
}


def chain(n, state_name='x', action='a', start=None, clip=True, can_stay=True):
    if start is None:
        start = n // 2
    else:
        start -= 1

    start = encode_int(n, 1 << start, signed=False)

    x = atom(n, state_name, signed=False)
    a = atom(2, action, signed=False)

    backward, forward = a[0], a[1]
    x2 = ite(forward, x << 1, x >> 1)

    stay = atom(1, 1, signed=False)
    if clip:
        stay = (x2 == 0)
    if can_stay:
        stay |= ~(forward | backward)
    if clip or can_stay:
        x2 = ite(stay, x, x2)

    circ = x2.aigbv['o', {x2.output: state_name}]
    return circ.feedback(
        inputs=[state_name],
        outputs=[state_name],
        initials=[start],
        keep_outputs=True
    )


def gridworld(n, start=(None, None), compressed_inputs=False):
    # Gridworld is 2 synchronized chains.
    circ = chain(n, 'x', 'ax', start[1]) | chain(n, 'y', 'ay', start[0])
    circ <<= split_gate('a', 2, 'ay', 2, 'ax')       # Combine inputs.
    x = BV.uatom(circ.omap['x'].size, 'x')
    y = BV.uatom(circ.omap['y'].size, 'y')
    circ >>= y.concat(x).with_output('state').aigbv  # Combine outputs.

    if compressed_inputs:
        uncompress = lookup(
            2, 4, COMPRESSION_MAPPING, 'a', 'a',
            in_signed=False, out_signed=False
        )
        circ <<= uncompress

    # Wrap using aiger discrete add encoding + valid inputs.
    actions_map = ACTIONS_C if compressed_inputs else ACTIONS
    action_encoding = aiger_discrete.Encoding(
        encode=actions_map.get,
        decode=actions_map.inv.get,
    )
    state_encoding = aiger_discrete.Encoding(
        encode=lambda s: s.yx,
        decode=lambda yx: G.GridState(yx, n),
    )

    func = aiger_discrete.from_aigbv(
        circ,
        input_encodings={'a': action_encoding},
        output_encodings={'state': state_encoding},
    )
    if not compressed_inputs:
        action = BV.uatom(4, 'a')
        is_1hot = (action != 0) & ((action & (action - 1)) == 0)
        func = func.assume(is_1hot)
    return func


__all__ = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'gridworld', 'chain']
