import operator as op
from functools import reduce

from aigerbv import atom


def sensor(n, color_mapping):
    x, y = atom(n, 'x', signed=False), atom(n, 'y', signed=False)

    def color_pred(color, coords):
        exp = reduce(op.or_, ((x == cx) & (y == cy) for cx, cy in coords))
        return exp.aigbv['o', {exp.output: color}]

    return reduce(op.or_, (color_pred(*kv) for kv in color_mapping.items()))
