"""Convert images into circloO objects."""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import numba
import subprocess


# MAIN FUNCTIONS #######################################################################################################

def image_to_circloo(img_path, downsample_factor,
                     start_x, start_y, size=1, start_line=-1,
                     threshold=.5, channel_weights=(1, 1, 1),
                     reduce_objects=True, show_img=True):
    """

    :param img_path:            Path of input image
    :param downsample_factor:   Factor by which to decrease image size; 1 for no change
    :param start_x:             Initial x coordinate (left)
    :param start_y:             Initial y coordinate (top)
    :param size:                Pixel size
    :param start_line:          Line enumeration; -1 to turn off
    :param threshold:           When reducing from rgb to grayscale, threshold of average value
    :param channel_weights:     When reducing from rgb to grayscale, weighting to average the value
    :param reduce_objects:      Uses optimization algorithms if True
    :param show_img:            Shows the dithered image if True
    :return:                String of circloO objects (w/o header)
    """
    # Open Image.
    img = Image.open(f"{img_path}")

    # Convert to numpy array.
    data = np.array(img).astype(np.float32) / 255   # normalize values as floats b/w 0 & 1
    if len(data.shape) == 2:    # add new channel if B&W image to preserve algorithms
        data = data[:, :, np.newaxis]

    data_smaller = downsample(data, downsample_factor)
    data_adjusted = floyd_steinberg(data_smaller)

    if show_img:
        plt.imshow(data_adjusted[:, :, 0], cmap='Greys_r')
        plt.show()

    if reduce_objects:
        data_single_channel = reduce_channels(data_adjusted, threshold=threshold, channel_weights=channel_weights)
        data_reduced = greedy_decomposition(data_single_channel)
        return reduced_build(data_reduced, start_x=start_x, start_y=start_y, size=size, start_line=start_line)
    else:
        return build(data_adjusted, threshold=threshold, channel_weights=channel_weights,
                     start_x=start_x, start_y=start_y, size=size, start_line=start_line)


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
                    image[i + 1, j, c] += (7 / 24) * err  # Original factor from paper: 7/16
                if j < ly - 1:
                    image[i, j + 1, c] += (5 / 24) * err  # Original: 5/16
                    if i > 0:
                        image[i - 1, j + 1, c] += (1 / 24) * err  # Original: 1/16
                    if i < lx - 1:
                        image[i + 1, j + 1, c] += (3 / 24) * err  # Original: 3/16
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


# OPTIMIZATION #########################################################################################################

def reduce_channels(arr: np.array, threshold=.5, channel_weights=(1, 1, 1)):
    """Convert rgb binary image into greyscale (with an extra channel for greedy_decomposition() function)."""
    new_arr = np.zeros((arr.shape[0], arr.shape[1], 2))

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            values = arr[i, j]
            avg = ((values[0] * channel_weights[0]
                    + values[1] * channel_weights[1]
                    + values[2] * channel_weights[2])
                   / sum(channel_weights))

            new_arr[i, j, 0] = 1 if avg <= threshold else 0

    return new_arr


def reduced_build(arr: np.array, start_x=1500, start_y=1500, size=1, start_line=-1):
    """Convert a reduced image array into a string of circloO objects."""
    text = []
    xpos = 0
    ypos = 0
    cur_line = 0

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            x_factor = arr[i, j, 0]
            y_factor = arr[i, j, 1]

            if x_factor > 0:
                text.append(f"b {xpos + start_x + size * x_factor} {ypos + start_y + size * y_factor} {size * x_factor} {size * y_factor} 0\n")

                if start_line >= 0:
                    text.append(f"< {cur_line}\n")
                    cur_line += 1

            xpos += 2 * size

        xpos = 0
        ypos += 2 * size

    return ''.join(text)


def greedy_decomposition(arr: np.array):
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


# FILES & ADB ##########################################################################################################

def text_to_file(output_path, text):
    """Convert a string of text into a file."""
    f = open(output_path, 'w')
    f.writelines(text)


def push_to_android(file_path, destination='/sdcard'):
    """
    Pushes a file to an Android device using ADB.
    """
    try:
        command = ['adb', 'push', file_path, destination]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"File successfully pushed to {destination} folder.")
        else:
            print(f"Error pushing file: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")


# EXAMPLE CODE #########################################################################################################

txt = image_to_circloo("mona_lisa.webp", 1, 1500, 1500, start_line=0)
print(txt)
text_to_file("circloO_image.txt", txt)
# push_to_android("circloO_image.txt", destination='/sdcard')   # ADB should be installed before use
