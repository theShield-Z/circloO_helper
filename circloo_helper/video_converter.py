"""Convert videos into circloO objects."""

import numpy as _np
import cv2 as _cv
from .objects import RectangleGenerator as _Gen


# DITHERING PATTERNS ###################################################################################################

BAYER_MATRIX_8X8 = (1 / 64) * _np.array([
    [ 0, 48, 12, 60,  3, 51, 15, 63],
    [32, 16, 44, 28, 35, 19, 47, 31],
    [ 8, 56,  4, 52, 11, 59,  7, 55],
    [40, 24, 36, 20, 43, 27, 39, 23],
    [ 2, 50, 14, 62,  1, 49, 13, 61],
    [34, 18, 46, 30, 33, 17, 45, 29],
    [10, 58,  6, 54,  9, 57,  5, 53],
    [42, 26, 38, 22, 41, 25, 37, 21]
    ])

LINE_DITHER_8X8 = (1 / 64) * _np.array([
    [ 0,  1,  2,  3,  4,  5,  6,  7],
    [32, 33, 34, 35, 36, 37, 38, 39],
    [16, 17, 18, 19, 20, 21, 22, 23],
    [48, 49, 50, 51, 52, 53, 54, 55],
    [ 8,  9, 10, 11, 12, 13, 14, 15],
    [40, 41, 42, 43, 44, 45, 46, 47],
    [24, 25, 26, 27, 28, 29, 30, 31],
    [56, 57, 58, 59, 60, 61, 62, 63],
])

DOTTED_LINE_DITHER_8X8 = (1 / 64) * _np.array([
    [ 0, 16,  1, 17,  2, 18,  3, 19],
    [32, 48, 33, 49, 34, 50, 35, 51],
    [ 8, 24,  9, 25, 10, 26, 11, 27],
    [40, 56, 41, 57, 42, 58, 43, 59],
    [ 4, 20,  5, 21,  6, 22,  7, 23],
    [36, 52, 37, 53, 38, 54, 39, 55],
    [12, 28, 13, 29, 14, 30, 15, 31],
    [44, 60, 45, 61, 46, 62, 47, 63],
])


# MAIN FUNCTION ########################################################################################################

def video_to_circloo(video_path: str, frame_size: tuple[int, int], frame_skip: int, fps: float,
                     start_x: float, start_y: float, size: float = 1,
                     threshold: float = .5, channel_weights: tuple[float, float, float] = (1, 1, 1),
                     dither_pattern: _np.array = LINE_DITHER_8X8, start_off: bool = False,
                     show_img: bool = False, wait_key: int = 1,
                     turn_off_noanim: bool = False):
    """
    Converts a video into circloO objects via dithering & grayscale conversion.
    :param video_path:          Path to video for conversion.
    :param frame_size:          Width x Height of video after conversion.
    :param frame_skip:          Number of frames to skip. 1 for no change.
    :param fps:                 FPS of video after conversion.
    :param start_x:             X coordinate of in-game display.
    :param start_y:             Y coordinate of in-game display.
    :param size:                Size of each pixel in-game; default is 1.
    :param threshold:           Threshold for grayscale conversion; default is 0.5
    :param channel_weights:     Weights for RGB channels; default is (1, 1, 1).
    :param dither_pattern:      Pattern for dithering video; None for no dithering; default is BAYER_MATRIX_8X8.
    :param start_off:           If True, the video does not start playing when the level is started.
    :param show_img:            If True, displays video as it is converted; faster when False; default is False
    :param wait_key:            Time to wait between displaying of each frame; default is 1; automatically set to 0 if show_img is False
    :param turn_off_noanim:     Turns off noanim; somewhat reduces file size, but makes end result less viewable
    :return:                List of circloO objects
    """

    if not show_img:
        # Set wait_key to 0 if not displaying the video
        #   wait_key is necessary for displaying video, but slows the program significantly when not needed.
        wait_key = 0

    # Open video.
    cap = _cv.VideoCapture(video_path)
    total_frames = cap.get(_cv.CAP_PROP_FRAME_COUNT)

    if not cap.isOpened():
        raise Exception("Cannot open video file")

    frame_count = 0
    processed_frames = []

    # Loop through video frames.
    while True:
        ret, frame = cap.read()

        if not ret:
            print("End of video or can't reach frame. Converting to circloO...")
            break

        if frame_count % frame_skip == 0:
            # Process frame.
            small_frame = _cv.resize(frame, dsize=frame_size)
            image = small_frame.astype(_np.float32) / 255
            dithered_image = ordered_dither(image, dither_pattern)
            binary_image = binarize(dithered_image, threshold, channel_weights)
            reduced_image = greedy_decomposition(binary_image)
            processed_frames.append(reduced_image)

            if show_img:
                _cv.imshow("circloO Video is Processing...", (1 - binary_image).astype(_np.uint8) * 255)
            else:
                print(f"Processing... ({frame_count}/{total_frames})")

        _cv.waitKey(wait_key)
        frame_count += 1

    cap.release()
    _cv.destroyAllWindows()

    time_reduced = greedy_time(processed_frames)
    objs = reduced_build(time_reduced, start_x, start_y, size, fps, start_off, turn_off_noanim=turn_off_noanim)

    print(f"Successfully converted {video_path} to circloO objects.")

    return objs


# IMAGE PROCESSING #####################################################################################################

def ordered_dither(image: _np.array, pattern: _np.array = BAYER_MATRIX_8X8):
    """Ordered Dithering using pattern matrix."""

    if pattern is None:
        return image

    height, width, _ = image.shape

    threshold_map = _np.tile(pattern, (height // pattern.shape[0] + 1, width // pattern.shape[1] + 1))[:height, :width]
    threshold_map = threshold_map[:, :, _np.newaxis]

    dithered_image = (image > threshold_map)

    return dithered_image


def binarize(arr: _np.array, threshold: float = 0.5, channel_weights: tuple[float, float, float] = (1, 1, 1)):
    """Convert float32 image to binary grayscale + extra channels for reduction algorithms."""
    avg = _np.dot(arr[:, :, :3], channel_weights) / sum(channel_weights)
    binary_image = (avg <= threshold).astype(_np.float32)
    return binary_image


# CONVERSION TO CIRCLOO ################################################################################################

def greedy_decomposition(arr: _np.array):
    """Reduce a binary image array into an array corresponding to the length & width of each pixel."""
    temp_arr = arr.copy()
    arr = _np.zeros((arr.shape[0], arr.shape[1], 3))
    arr[:, :, 0] = temp_arr

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


def greedy_time(frames: list[_np.array, ...]):
    """Further reduce a list of greedily-reduced frames temporally."""

    for r in range(frames[0].shape[0]):

        for c in range(frames[0].shape[1]):

            check_point = -1
            merging = False
            for f in range(len(frames)):

                cur = frames[f][r, c, :2]

                if not merging and _np.any(cur != 0):
                    # Non-zero Value.
                    frames[f][r, c, 2] = 1

                if f != len(frames) - 1:
                    nxt = frames[f + 1][r, c, :2]

                    if not merging and _np.all(cur == nxt) and _np.all(cur != 0):
                        # First equal sets in a row.
                        merging = True
                        check_point = f

                        # Merge the equal sets.
                        frames[f + 1][r, c, :] = 0
                        frames[f][r, c, 2] += 1

                    elif merging and _np.all(cur == nxt) and _np.all(cur != 0):
                        # Continuing equal sets in a row.
                        frames[f + 1][r, c, :] = 0
                        frames[f][r, c, :] = 0
                        frames[check_point][r, c, 2] += 1

                    elif merging and _np.any(cur != nxt):
                        # End of equal set sequence.
                        merging = False

    return frames


def reduced_build(frames: list[_np.array, ...], start_x: float = 1500, start_y: float = 1500, size: float = 1,
                  fps: float = 2, start_off: bool = False, turn_off_noanim: bool = False):
    """Convert a reduced image array into a list of circloO objects."""
    objs = []
    xpos = 0
    ypos = 0
    no_fade = not turn_off_noanim

    for f in range(len(frames)):
        for i in range(frames[f].shape[0]):
            for j in range(frames[f].shape[1]):
                x_factor = frames[f][i, j, 0]
                y_factor = frames[f][i, j, 1]
                t_factor = frames[f][i, j, 2]

                if x_factor > 0:
                    size_x = size * x_factor * 2
                    size_y = size * y_factor * 2
                    x_coord = xpos + start_x
                    y_coord = ypos + start_y
                    on_time = t_factor / fps
                    delay = (fps + f) / fps

                    objs.append(_Gen(x_coord, y_coord, size_x, size_y, density=0, damping=0,
                                     disappear_after=on_time, wait_between=9999, init_delay=delay,
                                     start_off=start_off, no_fade=no_fade))

                xpos += 2 * size

            xpos = 0
            ypos += 2 * size

        ypos = 0

    return objs



