from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import masks.Gradient as masks
from noise.Perlin import Perlin


def worldGen(seed, continant_size=.18, seaLevel=.15, flatness=1.3):
    noise_gen = Perlin(seed)
    width = 200
    height = 200

    # ----- Generating the outline shape for major landmasses
    gridArray = []
    # base perlin feature size
    gridArray.append(noise_gen.generate_grid(width, height, continant_size, 1.8, .9))
    gridArray.append(noise_gen.generate_grid(width, height, .7, .5, .9))
    gridArray.append(noise_gen.generate_grid(width, height, .9, .2, .4))
    landmass = noise_gen.mix(gridArray)
    # gradiant though which we remove landmass by the poles
    lingrad = masks.linearGradient((-0, 1), (0, height), 50, width, height)
    lingrad += masks.linearGradient((-0, 1), (0, 0), 50, width, height)
    rlingrad = (lingrad * -1) + 1
    landmass *= rlingrad
    # sea level + cap, to avoid overly positive values
    landmass[landmass < seaLevel] = 0
    landmass[landmass > 1] = 1

    # ----- Giving the landmasses detail/texture
    gridArray = []
    gridArray.append(noise_gen.generate_grid(width, height, .3, .8, 3))
    gridArray.append(noise_gen.generate_grid(width, height, .5, .8, .6))
    gridArray.append(noise_gen.generate_grid(width, height, 1, .6, .6))
    gridArray.append(noise_gen.generate_grid(width, height, 3, .3, .6))

    result = (noise_gen.mix(gridArray) * landmass) / flatness


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




seed = 5456  # random. Whatever you'd like.
seaLevel = .3  # between .1 and .6 (.15 default) : Higher is more ocean.
flatness = 1.3  # between .5 and 3 (1.2 default) : Higher value = flatter/less elevation.
continant_size = .18
worldGen(seed, continant_size, seaLevel, flatness)
