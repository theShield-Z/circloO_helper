from copy import copy
from typing import Callable

import numpy as np
import imageio.v3 as iio
from PIL import Image

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

        try:
            metadata = iio.immeta(self._filepath)
        except Exception as e:
            raise ValueError(f"Can not read video at {self._filepath}")

        source_fps = float(metadata['fps'])

        # Count source frames.
        total_source_frames = 0
        for _ in iio.imiter(self._filepath):
            total_source_frames += 1

        source_duration = total_source_frames / source_fps      # in seconds

        total_target_frames = int(source_duration * self._fps)
        frame_duration = source_duration / total_target_frames  # in seconds

        # Set up video display
        if self._show_img:
            import matplotlib.pyplot as plt

            preview_im = None
            plt.ion()
            fig, ax = plt.subplots()
            ax.axis('off')
            fig.canvas.manager.set_window_title('Processing video...')

        processed_frames = []

        frame_step = source_fps / self._fps
        next_source_frame = 0

        for source_frame_idx, frame_rgb in enumerate(iio.imiter(self._filepath)):

            # Skip frames to achieve desired fps.
            if source_frame_idx < int(next_source_frame):
                continue
            next_source_frame += frame_step

            # Processing.
            frame_resized = np.asarray(
                Image.fromarray(frame_rgb).resize(
                    self._resolution,
                    Image.Resampling.BILINEAR
                )
            )

            data = frame_resized.astype(np.float32) / 255
            data_dithered = self._ditherer(data)
            data_avg = np.average(data_dithered[:, :, :3], axis=2, weights=np.asarray(self._channel_weights))
            pix_arr = np.where(data_avg >= self._threshold, 0, 1)

            processed_frames.append(pix_arr)

            if len(processed_frames) >= total_target_frames:
                break

            # Display video as it processes.
            if self._show_img:
                img = (1 - pix_arr).astype(np.uint8) * 255

                if preview_im is None:
                    preview_im = ax.imshow(
                        img,
                        cmap='gray',
                        vmin=0,
                        vmax=255
                    )
                else:
                    preview_im.set_data(img)

                fig.canvas.draw_idle()
                fig.canvas.flush_events()
                plt.pause(0.001)

        if self._show_img:
            plt.close(fig)

        return processed_frames, frame_duration
