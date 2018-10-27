from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import masks.Gradient as masks
from noise.Perlin import Perlin


def worldGen(seed, seaLevel=.15, flatness=1.2):
    noise_gen = Perlin(seed)
    width = 200
    height = 200
    gridArray = []

    #  land features
    gridArray.append(noise_gen.generate_grid(width, height, .6, 2, 1))

    # minor land features
    gridArray.append(noise_gen.generate_grid(width, height, .2, .5, 1))
    gridArray.append(noise_gen.generate_grid(width, height, .5, .4, .5))

    # detail
    gridArray.append(noise_gen.generate_grid(width, height, 2, .6, .1))
    gridArray.append(noise_gen.generate_grid(width, height, 5, .3, .1))

    # Feature blend
    grid = (noise_gen.mix(gridArray) + .5)

    # Constraints in the form of continent outlines + constraints away from the poles
    constraint = (masks.gradMask(width, height, 80) * noise_gen.generate_grid(width, height, .18, 1.8, .9))

    # Conforming land features to constraints
    landmass = grid * constraint

    # Post-landmass re-brightening of the central continants
    result = landmass * (masks.igradMask(width, height, 40) * 2)

    # setting a lower bound on heightmap to simulate oceans. This is essentially defining sea level
    result[result <= seaLevel] = 0
    result = result / flatness

    colors = [(0, .15, .4), (0, .4, .3), (0, .45, .3), (0, .5, .1), (0, .55, .1), (0, .6, .1), (0, .6, .1),
              (.7, .7, .7), (.7, .75, .7), (1, 1, 1), (1, 1, 1)]
    n_bin = 100  # Discretizes the interpolation into bins
    cmap_name = 'my_list'
    # Create the colormap
    cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
    # Fewer bins will result in "coarser" colomap interpolation
    im = plt.imshow(result, interpolation='nearest', origin='lower', cmap=cm, vmin=0, vmax=1)
    plt.colorbar(im)

    plt.show()


# ---------------------------------
# ---  RUN THIS -------------------
# -- play button in upper right ---
# OOH nice
# ---------------------------------

seed = 5456  # random. Whatever you'd like.
seaLevel = .15  # between .1 and .6 (.15 default) : Higher is more ocean.
flatness = 1.2  # between .5 and 3 (1.2 default) : Higher value = flatter/less elevation.
worldGen(seed, seaLevel, flatness)
