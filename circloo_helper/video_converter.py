from copy import copy
import numpy as np
import cv2 as cv
import numba

from .object import CustomObject
from .object_types import Generator
from .object_shapes import Rectangle
from .tools import translate, dimensions


# DITHERING PATTERNS ###################################################################################################

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


class CHVideo(CustomObject):
    def __init__(self,
                 filepath: str,
                 obj: Generator,
                 resolution: tuple[int, int],
                 fps: int | float,
                 threshold: int | float = .5,
                 channel_weights: tuple[int | float, int | float, int | float] = (1, 1, 1),
                 show_img: bool = True):
        super().__init__()
        self._filepath = filepath

        self._obj = obj
        self._obj.wait_between = 9999

        self._resolution = resolution
        self._fps = fps

        self._threshold = threshold
        self._channel_weights = channel_weights
        self._show_img = show_img

        self._is_already_built = False

    def build_objs(self):
        if self._is_already_built:
            return self._obj_cache

        super().build_objs()

        cap = cv.VideoCapture(self._filepath)
        if not cap.isOpened():
            raise ValueError(f"Can not read video at {self._filepath}")

        total_source_frames = cap.get(cv.CAP_PROP_FRAME_COUNT)
        source_fps = cap.get(cv.CAP_PROP_FPS)
        source_duration = total_source_frames / source_fps

        total_target_frames = int(source_duration * self._fps)
        frame_duration = source_duration / total_target_frames

        processed_frames = []

        for target_frame_idx in range(total_target_frames):
            # Map target frame to source frame.
            source_frame_idx = int(target_frame_idx * (source_fps / self._fps))

            if source_frame_idx >= total_source_frames:
                # Ensure video length is not overshot.
                break

            # Jump to mapped source frame.
            cap.set(cv.CAP_PROP_POS_FRAMES, source_frame_idx)

            ret, frame = cap.read()

            if not ret:
                break

            # Processing.
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame_resized = cv.resize(frame_rgb, self._resolution)
            data = frame_resized.astype(np.float32) / 255
            data_dithered = self.ordered_dither(data)
            data_avg = np.average(data_dithered[:, :, :3], axis=2, weights=np.asarray(self._channel_weights))
            pix_arr = np.where(data_avg >= self._threshold, 0, 1)

            processed_frames.append(pix_arr)

            # Display video as it processes.
            if self._show_img:
                cv.imshow("circloO Video is Processing...", (1 - pix_arr).astype(np.uint8) * 255)
                cv.waitKey(1)
                # cv.waitKey(int(frame_duration * 1000))    # Show video in real time
            else:
                pass
                # cv.waitKey(0)

        # Append to obj_cache.
        obj_width, obj_height = dimensions(self._obj)
        for rect in self._rectangle_decomposer(np.asarray(processed_frames)):
            (x, y, f), (width, height, duration) = rect

            obj = translate(self._obj, x * obj_width, y * obj_height)
            obj.disappear_after = frame_duration * duration
            obj.init_delay = f * frame_duration

            if isinstance(obj, Rectangle):
                obj.width *= width
                obj.height *= height
            self._obj_cache.append(obj)

        self._is_already_built = True
        return self._obj_cache

    @staticmethod
    def ordered_dither(image: np.array, pattern: np.array = BAYER_MATRIX_8X8):
        """Ordered Dithering using pattern matrix."""

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

    @staticmethod
    @numba.njit
    def _rectangle_decomposer(arr: np.array):
        """
        Decomposes a 3D numpy binary array into the minimum number of spanning rectangles
        using a depth->width->height greedy algorithm
        :return: Generator that yields each rectangle as ((x, y, z), (width, height, depth))
        """
        arr = arr.copy()
        a, b, c = arr.shape
        # a -> number of frames
        # b -> height of frame
        # c -> width of frame

        for j in range(b):
            for k in range(c):
                for i in range(a):

                    cur = arr[i, j, k]

                    if cur == 0:
                        continue

                    # Find depth.
                    depth = 1
                    while i + depth < a and arr[i + depth, j, k] > 0:
                        depth += 1

                    # Find width.
                    width = 1
                    while k + width < c:
                        if np.all(arr[i:i + depth, j, k + width]):
                            width += 1
                        else:
                            break

                    # Find height.
                    height = 1
                    while j + height < b:
                        if np.all(arr[i:i + depth,
                                      j + height,
                                      k:k + width]):
                            height += 1
                        else:
                            break

                    yield (k, j, i), (width, height, depth)

                    # Clear the determined region so that it is not processed again.
                    arr[i: i + depth,
                        j: j + height,
                        k: k + width] = 0
