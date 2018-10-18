from itertools import product

import funcy as fn

from aiger_gridworld import sensor, utils


def test_sensor():
    color_mapping = {
        'yellow': {(0, 0), (0, 7), (7, 0), (7,7)},
        'red': (
            {(1, 0), (0, 1), (1, 1)} |
            {(6, 0), (6, 1), (7, 1)} |
            {(0, 4), (0, 5), (1, 4), (1, 5)} |
            {(6, 4), (6, 5), (7, 4), (7, 5)}
        ),
        'blue': (
            {(3, i) for i in range(2, 6)} |
            {(4, i) for i in range(2, 6)}
        ),
        'brown': (
            {(i, 0) for i in range(2, 6)} |
            {(i, 7) for i in range(2, 6)}
        ),
    }

    sens = sensor.sensor(3, color_mapping)
    all_points = product(range(7), range(7))
    colored = set.union(*color_mapping.values())

    for point in all_points:
        val = sens(utils.encode_point(point))[0]
        n_active = sum(fn.cat(val.values()))
        assert n_active == int(point in colored)

        for c in color_mapping.keys():
            if point in color_mapping[c]:
                assert val[c][0]
