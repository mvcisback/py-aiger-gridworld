import aiger_gridworld as G


EXPECTED = """
5 □ □ □ □ □
4 □ □ □ □ □
3 ▪ □ □ □ □
2 □ □ □ □ □
1 □ □ □ □ □
  1 2 3 4 5
"""


def test_vis():
    world = G.gridworld(5, (2, 3))
    state = world({'a': '←'})[0]['state']
    assert EXPECTED == state.board
