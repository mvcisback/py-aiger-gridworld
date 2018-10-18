import aigerbv


def _gridworld1d(n, state_name='x', action='a', start=0):
    x = aigerbv.atom(n, state_name, signed=False)
    a = aigerbv.atom(n, action)

    guard = (a != 1) | (x != 2**n - 1)
    guard &= (a != -1) | (x != 0)
    x += guard.repeat(n) & a

    circ = x.aigbv['o', {x.output: state_name}]
    return circ.feedback(
        inputs=[state_name],
        outputs=[state_name],
        initials=[start],
        keep_outputs=True
    )


def gridworld(n, start=(0, 0)):
    circ = _gridworld1d(n, 'x', 'ax', start[0]) \
        | _gridworld1d(n, 'y', 'ay', start[1])

    ax = aigerbv.lookup(mapping={0: 0, 1: 1, 2: 0, 3: -1},
                        input='tmp1',
                        output='ax',
                        inlen=2,
                        outlen=n,
                        in_signed=False)

    ay = aigerbv.lookup(mapping={0: 1, 1: 0, 2: -1, 3: 0},
                        input='tmp2',
                        output='ay',
                        inlen=2,
                        outlen=n,
                        in_signed=False)

    action = aigerbv.tee(2, {'a': ('tmp1', 'tmp2')}) >> (ax | ay)
    return action >> circ
