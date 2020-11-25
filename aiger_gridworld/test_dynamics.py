from aiger_gridworld import dynamics


def move(action, x=None, y=None):
    g = dynamics.gridworld(5, start=(x, y))

    pos, _ = g({'a': action})
    return pos['state']


def board_test(state, x, y):
    assert state.x == x
    assert state.y == y


def test_move():
    board_test(move('←'), 2, 3)
    board_test(move('→'), 4, 3)
    board_test(move('↑'), 3, 4)
    board_test(move('↓'), 3, 2)

    # TEST clipping.

    board_test(move('←', 2, 2), 1, 2)
    board_test(move('←', 1, 2), 1, 2)

    board_test(move('↓', 2, 2), 2, 1)
    board_test(move('↓', 2, 1), 2, 1)

    board_test(move('→', 4, 4), 5, 4)
    board_test(move('→', 5, 4), 5, 4)

    board_test(move('↑', 4, 4), 4, 5)
    board_test(move('↑', 4, 5), 4, 5)
