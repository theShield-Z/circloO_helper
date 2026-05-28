from copy import copy
from typing import Callable
import numpy as np
import cv2 as cv

from .object import CustomObject
from .object_types import Generator
from .dithering import LINE_DITHER_8X8, ordered_dither
from .pixel_builder import Pixels


class CHVideo(CustomObject):
    """circloO Helper Video"""

    def __init__(self,
                 filepath: str,
                 obj: Generator,
                 resolution: tuple[int, int],
                 fps: int | float,
                 threshold: int | float = .5,
                 channel_weights: tuple[int | float, int | float, int | float] = (1, 1, 1),
                 ditherer: Callable[[np.array], np.array] = lambda x: ordered_dither(x, LINE_DITHER_8X8),
                 show_img: bool = True):
        """
        Converts a video into circloO objects via dithering & grayscale conversion.
        :param filepath:            Path to input image
        :param obj:                 Object to be tiled into video. Top-left object of the video has obj's coordinates.
        :param resolution:          Output resolution of video in pixels as (width, height).
        :param fps:                 Output frames per second of video.
        :param threshold:           Threshold for grayscale conversion; default is 0.5
        :param channel_weights:     Weights for RGB channels; default is (1, 1, 1)
        :param ditherer:            Dithering function (found in `dithering` module); default is ordered with a line pattern
        :param show_img:            If True, displays the video as it processes; default is True
        """
        super().__init__()
        self._filepath = filepath

        self._obj = obj

        self._resolution = resolution
        self._fps = fps

        self._threshold = threshold
        self._channel_weights = channel_weights
        self._show_img = show_img

        self._ditherer = ditherer

        self._is_already_built = False

    def build_objs(self):
        if self._is_already_built:
            return self._obj_cache

        super().build_objs()

        processed_frames, frame_duration = self._process_video()

        # Convert to Objects
        obj = copy(self._obj)
        obj.disappear_after = frame_duration
        obj.init_delay = frame_duration
        self._obj_cache.extend(Pixels(processed_frames, obj).build_objs())

        self._is_already_built = True
        return self._obj_cache

    def _process_video(self):
        """
        Processes the video at self._filepath.
        Returns as a tuple the processed frames and the duration of each frame in seconds.
        """
        cap = cv.VideoCapture(self._filepath)
        if not cap.isOpened():
            raise ValueError(f"Can not read video at {self._filepath}")

        total_source_frames = cap.get(cv.CAP_PROP_FRAME_COUNT)
        source_fps = cap.get(cv.CAP_PROP_FPS)
        source_duration = total_source_frames / source_fps      # in seconds

        total_target_frames = int(source_duration * self._fps)
        frame_duration = source_duration / total_target_frames  # in seconds

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
            data_dithered = self._ditherer(data)
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

        return processed_frames, frame_duration
