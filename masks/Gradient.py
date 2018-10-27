import numpy as np

import custom_math.helpers as mhelpers


# not currently used. Creates a circle.
def circleMask(width, height, falloff):
    grid = np.zeros(shape=(width, height))
    midpoint = (width / 2, height / 2)
    for x in range(width):
        for y in range(height):
            dist = mhelpers.dist_between_points(midpoint, (x, y))
            decay = np.square((dist) / falloff)
            grid[y][x] = (1 - decay)
    grid[grid > 1] = 1
    grid[grid < 0] = 0
    return grid


def linearGradient(vector, origin, falloff, width, height):
    vector = np.array(vector)
    origin = np.array(origin)
    vector_target = origin + vector
    perp_vector = mhelpers.perpendicular_vector(vector)
    perp_target = origin + perp_vector
    gradient_line = np.array([perp_target, origin])

    grid = np.zeros(shape=(width, height))

    for y in range(height):
        for x in range(width):
            gradient_intersect = mhelpers.closestPointOnLine(gradient_line, (x, y))
            dist = mhelpers.dist_between_points(gradient_intersect, (x, y))
            grid[y][x] = 1 - (dist / falloff)
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

            dist = mhelpers.dist_between_points(midpoint, (x, y))
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

            dist = mhelpers.dist_between_points(midpoint, (x, y))
            decay = dist / falloff
            grid[y][x] = (decay)

    grid[grid < .5] = .5
    return grid


# distance between 2 points.
