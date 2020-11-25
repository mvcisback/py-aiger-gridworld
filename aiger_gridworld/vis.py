import attr


def one_index(val):
    assert val != 0
    count = 0
    while True:
        if (val >> count) & 1:
            break
        count += 1
    return count


@attr.s(auto_attribs=True, frozen=True)
class GridState:
    yx: int
    dim: int

    @property
    def x(self):
        return one_index(self.yx) + 1

    @property
    def y(self):
        return one_index(self.yx >> self.dim) + 1

    def _row(self, row) -> str:
        x, y = self.x, self.y
        for col in range(1, self.dim + 1):
            yield ('▪' if y == row and x == col else '□')

    @property
    def board(self):
        buff = '\n'
        for row in range(self.dim, 0, -1):
            buff += f'{row} '
            buff += ' '.join(self._row(row)) + '\n'
        buff += '  ' + ' '.join(map(str, range(1, self.dim + 1))) + '\n'
        return buff


__all__ = ['GridState']
