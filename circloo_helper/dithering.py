"""
Includes both Floyd-Steinberg error diffusion dithering and Ordered dithering.

If you want to implement your own dithering function, the input parameter and return value of each should be an image with three channels as a numpy array.
Note that, if using ordered dithering for the `ditherer` parameter of CHVideo or CHImage, you must pass in the dithering pattern via a lambda function:
    e.g., ditherer=lambda x: ordered_dither(x, BAYER_MATRIX_8X8)

Ordered dithering patterns:
- BAYER_MATRIX_8X8 - Basic 8x8 Bayer matrix; recommended for images or small videos.
- LINE_DITHER_8X8 - Dithers in straight horizontal lines; recommended for large videos, since it maximizes the amount width-first rectangle decomposition algorithms help.
- DOTTED_LINE_DITHER - Similar to LINE_DITHER_8X8, but alternates the lines and positions for a little more detail; recommended for medium videos.
- You can also make your own pattern (they're just 2D numpy arrays :p)
"""

import numba
import numpy as np


# ORDERED PATTERNS #####################################################################################################

BAYER_MATRIX_8X8 = (1 / 64) * np.array([
    [ 0, 48, 12, 60,  3, 51, 15, 63],
    [32, 16, 44, 28, 35, 19, 47, 31],
    [ 8, 56,  4, 52, 11, 59,  7, 55],
    [40, 24, 36, 20, 43, 27, 39, 23],
    [ 2, 50, 14, 62,  1, 49, 13, 61],
    [34, 18, 46, 30, 33, 17, 45, 29],
    [10, 58,  6, 54,  9, 57,  5, 53],
    [42, 26, 38, 22, 41, 25, 37, 21]
    ])

LINE_DITHER_8X8 = (1 / 64) * np.array([
    [ 0,  1,  2,  3,  4,  5,  6,  7],
    [32, 33, 34, 35, 36, 37, 38, 39],
    [16, 17, 18, 19, 20, 21, 22, 23],
    [48, 49, 50, 51, 52, 53, 54, 55],
    [ 8,  9, 10, 11, 12, 13, 14, 15],
    [40, 41, 42, 43, 44, 45, 46, 47],
    [24, 25, 26, 27, 28, 29, 30, 31],
    [56, 57, 58, 59, 60, 61, 62, 63],
])

DOTTED_LINE_DITHER_8X8 = (1 / 64) * np.array([
    [ 0, 16,  1, 17,  2, 18,  3, 19],
    [32, 48, 33, 49, 34, 50, 35, 51],
    [ 8, 24,  9, 25, 10, 26, 11, 27],
    [40, 56, 41, 57, 42, 58, 43, 59],
    [ 4, 20,  5, 21,  6, 22,  7, 23],
    [36, 52, 37, 53, 38, 54, 39, 55],
    [12, 28, 13, 29, 14, 30, 15, 31],
    [44, 60, 45, 61, 46, 62, 47, 63],
])


# DITHERERS ############################################################################################################

@numba.njit
def floyd_steinberg(image: np.array):
    """Floyd-Steinberg dithering algorithm, adjusted to give more contrast.
    https://research.cs.wisc.edu/graphics/Courses/559-s2004/docs/floyd-steinberg.pdf"""
    image = image.copy()
    lx, ly, lc = image.shape
    for j in range(ly):
        for i in range(lx):
            for c in range(lc):
                rounded = round(image[i, j, c])
                err = image[i, j, c] - rounded
                image[i, j, c] = rounded
                if i < lx - 1:
                    image[i + 1, j, c] += (7 / 24) * err  # Original factor from paper: 7/16
                if j < ly - 1:
                    image[i, j + 1, c] += (5 / 24) * err  # Original: 5/16
                    if i > 0:
                        image[i - 1, j + 1, c] += (1 / 24) * err  # Original: 1/16
                    if i < lx - 1:
                        image[i + 1, j + 1, c] += (3 / 24) * err  # Original: 3/16
    return image


def ordered_dither(image: np.array, pattern: np.array):
    """Ordered Dithering using pattern matrix (a few basic patterns are included in the `dithering` module)."""
    image = image.copy()

    if pattern is None:
        return image

    height, width, _ = image.shape

    threshold_map = np.tile(
        pattern,
        (height // pattern.shape[0] + 1, width // pattern.shape[1] + 1)
    )[:height, :width]
    threshold_map = threshold_map[:, :, np.newaxis]

    dithered_image = (image > threshold_map)

    return dithered_image


def undither(image: np.array):
    """Do not perform any dithering. This is useful for purely black/white images."""
    return image.copy()
