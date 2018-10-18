from aiger_gridworld import dynamics


def test_gridworld_smoke():
    dynamics.gridworld(3, start=(2, 3))
