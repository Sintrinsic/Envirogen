import numpy as np


class Perlin:
    def __init__(self, seed):
        self.seed = seed

    # generates a grid of perlin noise based upon the input configuration
    def generate_grid(self, width, height, scale, contrast, brightness=1, seedMod=1):
        brightness = brightness - .5
        contrast = 1 / contrast
        scale = scale / 10
        xLin = [x * scale for x in range(width)]
        yLin = [y * scale for y in range(height)]
        x, y = np.meshgrid(xLin, yLin)

        grid = np.add(np.true_divide(self.perlin(x, y, self.seed * seedMod), contrast), brightness)
        return grid

    # Mixes a list of masks into their average.
    def mix(self, gridArray):
        sum = gridArray[0]
        for i in range(1, len(gridArray)):
            sum += gridArray[i]
            print("bob")

        output = sum / 2
        return output

    # ---------------- Stolen generic perlin methods below
    def perlin(self, x, y, seed):
        # permutation table
        np.random.seed(seed)
        p = np.arange(256, dtype=int)
        np.random.shuffle(p)
        p = np.stack([p, p]).flatten()
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
        n00 = self.gradient(p[p[xi] + yi], xf, yf)
        n01 = self.gradient(p[p[xi] + yi + 1], xf, yf - 1)
        n11 = self.gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
        n10 = self.gradient(p[p[xi + 1] + yi], xf - 1, yf)
        # combine noises
        x1 = self.lerp(n00, n10, u)
        x2 = self.lerp(n01, n11, u)  # FIX1: I was using n10 instead of n01
        return self.lerp(x1, x2, v)  # FIX2: I also had to reverse x1 and x2 here

    def lerp(self, a, b, x):
        "linear interpolation"
        return a + x * (b - a)

    def fade(self, t):
        "6t^5 - 15t^4 + 10t^3"
        return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3

    def gradient(self, h, x, y):
        "grad converts h to the right gradient vector and return the dot product with (x,y)"
        vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        g = vectors[h % 4]
        return g[:, :, 0] * x + g[:, :, 1] * y
