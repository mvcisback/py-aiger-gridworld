import aigerbv
import hypothesis.strategies as st
from hypothesis import given, settings

from aiger_gridworld import dynamics, utils


def move(x, y, action):
    g = dynamics.gridworld(2, start=(x, y))
    pos, _ = g({'a': aigerbv.encode_int(2, action, signed=False)})
    return utils.decode_point(pos)


@settings(max_examples=3)
@given(st.integers(min_value=0, max_value=2), st.integers(min_value=0, max_value=3))
def test_move_no_clip(x, y):
    x2, y2 = move(x, y, dynamics.EAST)
    assert x2 == x + 1
    assert y2 == y

    y, x = x, y
    x2, y2 = move(x, y, dynamics.NORTH)
    assert x2 == x
    assert y2 == y + 1
    
    y += 1
    x2, y2 = move(x, y, dynamics.SOUTH)
    assert x2 == x
    assert y2 == y - 1

    y, x = x, y
    x2, y2 = move(x, y, dynamics.WEST)
    assert x2 == x - 1
    assert y2 == y


def test_move_clip():
    assert move(0, 0, dynamics.WEST) == (0, 0)
    assert move(0, 0, dynamics.SOUTH) == (0, 0)
    assert move(3, 3, dynamics.NORTH) == (3, 3)
    assert move(3, 3, dynamics.EAST) == (3, 3)
