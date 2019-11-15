from aiger_bv import atom, ite, split_gate, encode_int, lookup


NORTH = (0, 0, 0, 1)
SOUTH = (0, 0, 1, 0)
EAST = (0, 1, 0, 0)
WEST = (1, 0, 0, 0)


def chain(n, state_name='x', action='a', start=None, clip=True, can_stay=True):
    if start is None:
        start = 1 << (n // 2)
    start = encode_int(n, start, signed=False)

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
    circ = chain(n, 'x', 'ax', start[0]) | chain(n, 'y', 'ay', start[1])
    circ <<= split_gate('a', 2, 'ax', 2, 'ay')
    if compressed_inputs:
        mapping = {0b00: 0b0001, 0b01: 0b0010, 0b10: 0b0100, 0b11: 0b1000}
        uncompress = lookup(
            2, 4, mapping, 'a', 'a', in_signed=False, out_signed=False
        )
        circ <<= uncompress

    return circ
