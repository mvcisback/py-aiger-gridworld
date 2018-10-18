import aigerbv


def encode_point(point):
    x, y = (aigerbv.encode_int(3, i, signed=False) for i in point)
    return {'x': tuple(x), 'y': tuple(y)}


def decode_point(point):
    xbits, ybits = point['x'], point['y']
    x, y = (aigerbv.decode_int(bits, signed=False) for bits in (xbits, ybits))
    return x, y
