"""Convert images into circloO objects."""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import numba


@numba.jit("f4[:,:,:](f4[:,:,:])", nopython=True, nogil=True)
def floyd_steinberg(image):
    """Floyd-Steinberg dithering algorithm, adjusted to give more contrast.
    https://research.cs.wisc.edu/graphics/Courses/559-s2004/docs/floyd-steinberg.pdf"""
    lx, ly, lc = image.shape
    for j in range(ly):
        for i in range(lx):
            for c in range(lc):
                rounded = round(image[i, j, c])
                err = image[i, j, c] - rounded
                image[i, j, c] = rounded
                if i < lx - 1:
                    image[i + 1, j, c] += (7 / 24) * err            # Original factor from paper: 7/16
                if j < ly - 1:
                    image[i, j + 1, c] += (5 / 24) * err            # Original: 5/16
                    if i > 0:
                        image[i - 1, j + 1, c] += (1 / 24) * err    # Original: 1/16
                    if i < lx - 1:
                        image[i + 1, j + 1, c] += (3 / 24) * err    # Original: 3/16
    return image


def downsample(image: np.array, factor: int):
    """Reduce image size by factor
    **USE THIS--DO NOT CRASH YOUR EDITOR"""
    return image[::factor, ::factor, :]


def build(arr: np.array, threshold=.5, channel_weights=(1, 1, 1), start_x=1500, start_y=1500, size=1, start_line=-1):
    """
    Convert image array into circloO objects.
    :param arr: Image
    :param threshold: Minimum average value of channels to place pixel
    :param channel_weights: Weighting applied to averaging channels together
    :param start_x: Initial x value (left)
    :param start_y: Initial y value (top)
    :param size: Size of each pixel
    :param start_line: Line enumeration; -1 to turn off
    :return: String of circloO objects (w/o header)
    """
    text = []
    xpos = 0
    ypos = 0
    cur_line = 0

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            values = arr[i, j]
            avg = ((values[0] * channel_weights[0]
                   + values[1] * channel_weights[1]
                   + values[2] * channel_weights[2])
                   / sum(channel_weights))

            if avg < threshold:
                text.append(f"b {xpos + start_x} {ypos + start_y} {size} {size} 0\n")

                if start_line >= 0:
                    text.append(f"< {cur_line}\n")
                    cur_line += 1

            xpos += 2 * size

        xpos = 0
        ypos += 2 * size

    return ''.join(text)


# EXAMPLE CODE #########################################################################################################

img = Image.open(r"mona_lisa.webp")

# Convert to numpy array.
data = np.array(img).astype(np.float32) / 255  # normalize values as floats between 0 & 1
if len(data.shape) == 2:  # add new channel if B&W image to keep algorithms the same
    data = data[:, :, np.newaxis]

# Adjust data.
data_smaller = downsample(data, 4)
data_adjusted = floyd_steinberg(data_smaller)

# Show adjusted image.
plt.imshow(data_adjusted[:, :, 0], cmap='Greys_r')
plt.show()

# Convert to circloO objects.
txt = build(data_adjusted, start_line=0)
print(txt)
