"""Convert images into circloO objects."""

import numpy as _np
from PIL import Image as _Image
import matplotlib.pyplot as _plt
from .objects import Rectangle as _Rectangle


# MAIN FUNCTIONS #######################################################################################################

def image_to_circloo(img_path, downsample_factor,
                     start_x, start_y, size=1,
                     threshold=.5, channel_weights=(1, 1, 1),
                     reduce_objects=True, show_img=True):
    """
    Converts an image into circloO objects via dithering & grayscale conversion.
    :param img_path:            Path to input image
    :param downsample_factor:   Factor to reduce image size; 1 for no change
    :param start_x:             Initial x-coordinate (left)
    :param start_y:             Initial y-coordinate (top)
    :param size:                Size of each pixel; default is 1
    :param threshold:           Threshold for grayscale conversion; default is 0.5
    :param channel_weights:     Weights for RGB channels; default is (1, 1, 1)
    :param reduce_objects:      If True, uses optimization algorithms--HIGHLY RECOMMENDED; default is True
    :param show_img:            If True, displays the processed image; default is True
    :return:                List of circloO objects
    """
    # Open Image.
    img = _Image.open(f"{img_path}")

    # Convert to numpy array.
    data = _np.array(img).astype(_np.float32) / 255   # normalize values as floats b/w 0 & 1
    if len(data.shape) == 2:    # add new channel if B&W image to preserve algorithms
        data = data[:, :, _np.newaxis]

    data_smaller = downsample(data, downsample_factor)
    data_adjusted = floyd_steinberg(data_smaller)

    if show_img:
        _plt.imshow(data_adjusted[:, :, 0], cmap='Greys_r')
        _plt.show()

    if reduce_objects:
        data_single_channel = reduce_channels(data_adjusted, threshold=threshold, channel_weights=channel_weights)
        data_reduced = greedy_decomposition(data_single_channel)
        return reduced_build(data_reduced, start_x=start_x, start_y=start_y, size=size)
    else:
        return build(data_adjusted, threshold=threshold, channel_weights=channel_weights,
                     start_x=start_x, start_y=start_y, size=size)


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
                    image[i + 1, j, c] += (7 / 24) * err  # Original factor from paper: 7/16
                if j < ly - 1:
                    image[i, j + 1, c] += (5 / 24) * err  # Original: 5/16
                    if i > 0:
                        image[i - 1, j + 1, c] += (1 / 24) * err  # Original: 1/16
                    if i < lx - 1:
                        image[i + 1, j + 1, c] += (3 / 24) * err  # Original: 3/16
    return image


def downsample(image: _np.array, factor: int):
    """Reduce image size by factor
    **USE THIS--DO NOT CRASH YOUR EDITOR"""
    return image[::factor, ::factor, :]


def build(arr: _np.array, threshold=.5, channel_weights=(1, 1, 1), start_x=1500, start_y=1500, size=1):
    """
    Convert image array into circloO objects.
    :param arr: Image
    :param threshold: Minimum average value of channels to place pixel
    :param channel_weights: Weighting applied to averaging channels together
    :param start_x: Initial x value (left)
    :param start_y: Initial y value (top)
    :param size: Size of each pixel
    :return: String of circloO objects (w/o header)
    """
    avg = _np.dot(arr[:, :, :3], channel_weights) / sum(channel_weights)
    rows, cols = _np.where(avg < threshold)

    objs = []

    for i, j in zip(rows, cols):
        xpos = j * 2 * size + start_x
        ypos = i * 2 * size + start_y
        objs.append(_Rectangle(xpos, ypos, size, size))

    return objs


# OPTIMIZATION #########################################################################################################

def reduce_channels(arr: _np.array, threshold=.5, channel_weights=(1, 1, 1)):
    """Convert rgb binary image into greyscale (with an extra channel for greedy_decomposition() function)."""
    avg = _np.dot(arr[:, :, :3], channel_weights) / sum(channel_weights)
    binary_image = (avg <= threshold).astype(_np.float32)

    new_arr = _np.zeros((arr.shape[0], arr.shape[1], 2), dtype=_np.float32)
    new_arr[:, :, 0] = binary_image
    return new_arr


def reduced_build(arr: _np.array, start_x=1500, start_y=1500, size=1):
    """Convert a reduced image array into a string of circloO objects."""
    objs = []
    xpos = 0
    ypos = 0

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            x_factor = arr[i, j, 0]
            y_factor = arr[i, j, 1]

            if x_factor > 0:
                objs.append(_Rectangle(xpos + start_x + size * x_factor, ypos + start_y + size * y_factor, size * x_factor, size * y_factor))

            xpos += 2 * size

        xpos = 0
        ypos += 2 * size

    return objs


def greedy_decomposition(arr: _np.array):
    """Reduce a binary image array into an array corresponding to the length & width of each pixel."""

    # Reduce pixels by merging side-to-side length.
    for i in range(arr.shape[0]):
        point = None

        for j in range(arr.shape[1]):
            cur = arr[i, j, 0]

            if cur == 1:
                if point is None:
                    point = (i, j, 0)
                else:
                    arr[point] += 1
                    arr[i, j, 0] = 0
            else:
                point = None

    # Merge vertically if equal horizontal length.
    for j in range(arr.shape[1]):
        point = None
        check_val = -1

        for i in range(arr.shape[0]):
            cur = arr[i, j, 0]

            if cur == 0:
                # Zero value, reset checker values
                point = None
                check_val = -1

            else:
                if point is None and check_val == -1:
                    # First nonzero point, store checker values
                    point = (i, j)
                    check_val = arr[point[0], point[1], 0]
                    arr[i, j, 1] = 1

                elif arr[i, j, 0] == check_val:
                    # Point below checker is equal, increase at check value, set cur to 0
                    arr[point[0], point[1], 1] += 1
                    arr[i, j, :] = 0

                else:
                    # Point below checker is new nonzero value, store new checker values
                    point = (i, j)
                    check_val = arr[point[0], point[1], 0]
                    arr[i, j, 1] = 1
    return arr
