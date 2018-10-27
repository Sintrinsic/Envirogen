import numpy as np


# not currently used. Creates a circle.
def circleMask(width, height, falloff):
    grid = np.zeros(shape=(width, height))
    midpoint = (width / 2, height / 2)
    for x in range(width):
        for y in range(height):
            dist = getDist(midpoint, (x, y))
            decay = np.square((dist) / falloff)
            grid[y][x] = (1 - decay)
    grid[grid > 1] = 1
    grid[grid < 0] = 0
    return grid


# Vertical gradient mask to cause the land to fall away toward the poles.
def gradMask(width, height, falloff):
    grid = np.zeros(shape=(width, height))
    midpoint = (width / 2, height / 2)
    for x in range(width):
        for y in range(height):
            midpoint = (x, height / 2)

            dist = getDist(midpoint, (x, y))
            decay = dist / falloff
            grid[y][x] = (1 - decay)
    grid[grid > 1] = 1
    grid[grid < 0] = 0
    return grid


# Inverse of the gradient mask, used to bring the edges back to full brighness,
# and make the fact that a gradient was used invisible.
def igradMask(width, height, falloff):
    grid = np.zeros(shape=(width, height))
    midpoint = (width / 2, height / 2)
    for x in range(width):
        for y in range(height):
            midpoint = (x, height / 2)

            dist = getDist(midpoint, (x, y))
            decay = dist / falloff
            grid[y][x] = (decay)

    grid[grid < .5] = .5
    return grid


# distance between 2 points.
def getDist(p1, p2):
    dist = np.sqrt(np.square((p2[0] - p1[0])) + np.square((p2[1] - p1[1])))
    return dist
