import aigerbv

def encode_point(point):
    x, y = (aigerbv.encode_int(3, i, signed=False) for i in point)
    return {'x': tuple(x), 'y': tuple(y)}
