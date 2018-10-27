import numpy as np


# copied from https://stackoverflow.com/questions/47177493/python-point-on-a-line-closest-to-third-point
def closestPointOnLine(line, point):
    line1 = line[0]
    line2 = line[1]
    x1, y1 = line1
    x2, y2 = line2
    x3, y3 = point
    dx, dy = x2 - x1, y2 - y1
    det = dx * dx + dy * dy
    a = (dy * (y3 - y1) + dx * (x3 - x1)) / det
    return x1 + a * dx, y1 + a * dy


def dist_between_points(p1, p2):
    dist = np.sqrt(np.square((p2[0] - p1[0])) + np.square((p2[1] - p1[1])))
    return dist


def perpendicular_vector(v):
    return np.array((v[1], v[0] * -1))
