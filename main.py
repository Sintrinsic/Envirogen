import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Noise_generator:
    def __init__(self,seed):
        self.seed = seed

    #generates a grid of perlin noise based upon the input configuration
    def generate_grid(self, width, height, scale, contrast, brightness=1, seedMod=1):
        brightness = brightness-.5
        contrast = 1 / contrast
        scale = scale / 10
        xLin = [x * scale for x in range(width)]
        yLin = [y * scale for y in range(height)]
        x,y = np.meshgrid(xLin,yLin)

        grid=np.add(np.true_divide(self.perlin(x,y,self.seed * seedMod), contrast),brightness)
        return grid


    #Mixes a list of masks into their average.
    def mix(self,gridArray):
        sum = gridArray[0]
        for i in range (1,len(gridArray)):
            sum += gridArray[i]
            print("bob")

        output = sum/2
        return output

    #not currently used. Creates a circle.
    def circleMask(self,width,height,falloff):
        grid = np.zeros(shape=(width,height))
        midpoint = (width/2,height/2)
        for x in range(width):
            for y in range(height):
                dist = self.getDist(midpoint,(x,y))
                decay = np.square((dist)/falloff)
                grid[y][x]=(1-decay)
        grid[grid>1]=1
        grid[grid<0] = 0
        return grid

    #Vertical gradient mask to cause the land to fall away toward the poles.
    def gradMask(self,width,height,falloff):
        grid = np.zeros(shape=(width,height))
        midpoint = (width/2,height/2)
        for x in range(width):
            for y in range(height):
                midpoint = (x, height / 2)

                dist = self.getDist(midpoint,(x,y))
                decay = dist/falloff
                grid[y][x]=(1-decay)
        grid[grid>1]=1
        grid[grid<0] = 0
        return grid

    #Inverse of the gradient mask, used to bring the edges back to full brighness,
    #and make the fact that a gradient was used invisible.
    def igradMask(self,width,height,falloff):
        grid = np.zeros(shape=(width,height))
        midpoint = (width/2,height/2)
        for x in range(width):
            for y in range(height):
                midpoint = (x, height / 2)

                dist = self.getDist(midpoint,(x,y))
                decay = dist/falloff
                grid[y][x]=(decay)

        grid[grid<.5] = .5
        return grid

    #distance between 2 points.
    def getDist(self,p1, p2):
        dist = np.sqrt(np.square((p2[0]-p1[0]))+np.square((p2[1]-p1[1])))
        return dist

    # ---------------- Stolen generic perlin methods below
    def perlin(self, x,y, seed):
        # permutation table
        np.random.seed(seed)
        p = np.arange(256,dtype=int)
        np.random.shuffle(p)
        p = np.stack([p,p]).flatten()
        # coordinates of the top-left
        xi = x.astype(int)
        yi = y.astype(int)
        # internal coordinates
        xf = x - xi
        yf = y - yi
        # fade factors
        u = self.fade(xf)
        v = self.fade(yf)
        # noise components
        n00 = self.gradient(p[p[xi]+yi],xf,yf)
        n01 = self.gradient(p[p[xi]+yi+1],xf,yf-1)
        n11 = self.gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
        n10 = self.gradient(p[p[xi+1]+yi],xf-1,yf)
        # combine noises
        x1 = self.lerp(n00,n10,u)
        x2 = self.lerp(n01,n11,u) # FIX1: I was using n10 instead of n01
        return self.lerp(x1,x2,v) # FIX2: I also had to reverse x1 and x2 here

    def lerp(self, a,b,x):
        "linear interpolation"
        return a + x * (b-a)

    def fade(self, t):
        "6t^5 - 15t^4 + 10t^3"
        return 6 * t**5 - 15 * t**4 + 10 * t**3

    def gradient(self, h,x,y):
        "grad converts h to the right gradient vector and return the dot product with (x,y)"
        vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        g = vectors[h % 4]
        return g[:, :, 0] * x + g[:, :, 1] * y


def worldGen(seed,seaLevel=.15, flatness=1.2):
    noise_gen = Noise_generator(seed)
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
    constraint =  (noise_gen.gradMask(width, height, 80) * noise_gen.generate_grid(width, height, .18, 1.8, .9))

    # Conforming land features to constraints
    landmass = grid * constraint

    # Post-landmass re-brightening of the central continants
    result = landmass * (noise_gen.igradMask(width, height, 40) * 2)

    # setting a lower bound on heightmap to simulate oceans. This is essentially defining sea level
    result[result<=seaLevel]=0
    result = result / flatness

    colors = [(0, .15, .4), (0, .4, .3),  (0, .45, .3),(0, .5, .1),(0, .55, .1),(0, .6, .1),(0, .6, .1), (.7, .7, .7),(.7, .75, .7),(1, 1, 1),(1, 1, 1)]
    n_bin = 100  # Discretizes the interpolation into bins
    cmap_name = 'my_list'
    # Create the colormap
    cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
    # Fewer bins will result in "coarser" colomap interpolation
    im = plt.imshow(result, interpolation='nearest', origin='lower', cmap=cm, vmin=0, vmax =1)
    plt.colorbar(im )

    plt.show()


# ---------------------------------
# ---  RUN THIS -------------------
# -- play button in upper right ---
# OOH nice
# ---------------------------------

seed = 5456     # random. Whatever you'd like.
seaLevel = .15  # between .1 and .6 (.15 default) : Higher is more ocean.
flatness = 1.2  # between .5 and 3 (1.2 default) : Higher value = flatter/less elevation.
worldGen(seed,seaLevel,flatness)