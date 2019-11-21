from aiger_gridworld import dynamics


def move(action, x=None, y=None):
    g = dynamics.gridworld(5, start=(x, y))

    pos, _ = g({'a': action})
    return pos['x'], pos['y']


def test_move():
    assert move(dynamics.WEST) == ((0, 1, 0, 0, 0), (0, 0, 1, 0, 0))
    assert move(dynamics.EAST) == ((0, 0, 0, 1, 0), (0, 0, 1, 0, 0))
    assert move(dynamics.SOUTH) == ((0, 0, 1, 0, 0), (0, 1, 0, 0, 0))
    assert move(dynamics.NORTH) == ((0, 0, 1, 0, 0), (0, 0, 0, 1, 0))

    x, y = (1, 0, 0, 0, 0), (1, 0, 0, 0, 0)
    assert move(dynamics.WEST, 1, 1) == (x, y)
    assert move(dynamics.SOUTH, 1, 1) == (x, y)

    x, y = (0, 0, 0, 0, 1), (0, 0, 0, 0, 1)
    assert move(dynamics.EAST, 5, 5) == (x, y)
    assert move(dynamics.NORTH, 5, 5) == (x, y)
