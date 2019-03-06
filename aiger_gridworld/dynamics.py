from aigerbv import atom, ite, split_gate



NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def chain(n, state_name='x', action='a', start=None, clip=True, can_stay=True):
    if start is None:
        start = 1 << (n // 2)
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


def gridworld(n, start=(None, None)):
    circ = chain(n, 'x', 'ax', start[0]) | chain(n, 'y', 'ay', start[1])
    return split_gate('a', 2, 'ax', 2, 'ay') >> circ
