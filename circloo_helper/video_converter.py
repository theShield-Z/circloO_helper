from copy import copy
from typing import Callable
import importlib.util

from .object import CustomObject
from .object_types import Generator
from .dithering import LINE_DITHER_8X8, ordered_dither
from .pixel_builder import Pixels

_default_show_img = importlib.util.find_spec('matplotlib') is not None


class CHVideo(CustomObject):
    """circloO Helper Video"""

    def __init__(self,
                 filepath: str,
                 obj: Generator,
                 resolution: tuple[int, int],
                 fps: int | float,
                 threshold: int | float = .5,
                 channel_weights: tuple[int | float, int | float, int | float] = (1, 1, 1),
                 ditherer: Callable[['np.array'], 'np.array'] = lambda x: ordered_dither(x, LINE_DITHER_8X8),
                 show_img: bool | None = None):
        """
        Converts a video into circloO objects via dithering & grayscale conversion.
        :param filepath:            Path to input image
        :param obj:                 Object to be tiled into video. Top-left object of the video has obj's coordinates.
        :param resolution:          Output resolution of video in pixels as (width, height).
        :param fps:                 Output frames per second of video.
        :param threshold:           Threshold for grayscale conversion; default is 0.5
        :param channel_weights:     Weights for RGB channels; default is (1, 1, 1)
        :param ditherer:            Dithering function (found in `dithering` module); default is ordered with a line pattern
        :param show_img:            If True, displays the processed image; if None, default value is True when matplotlib is installed and False otherwise; default is None
        """
        super().__init__()
        self.filepath = filepath

        self.obj = obj

        self.resolution = resolution
        self.fps = fps

        self.threshold = threshold
        self.channel_weights = channel_weights
        self.ditherer = ditherer

        self.show_img = show_img if show_img is not None else _default_show_img

    def _build_objs(self):
        super()._build_objs()

        processed_frames, frame_duration = self._process_video()

        # Convert to Objects
        obj = copy(self.obj)
        obj.disappear_after = frame_duration
        obj.init_delay = frame_duration
        self._obj_cache.extend(Pixels(processed_frames, obj).get_objs())

        return self._obj_cache

    def _process_video(self):
        """
        Processes the video at self._filepath.
        Returns as a tuple the processed frames and the duration of each frame in seconds.
        """

        try:
            import numpy as np
            import imageio.v3 as iio
            from PIL import Image
        except ImportError as e:
            raise ImportError("Install 'video' extras: numpy, imageio, imageio-ffmpeg, pillow") from e

        try:
            metadata = iio.immeta(self.filepath)
        except Exception as e:
            raise ValueError(f"Can not read video at {self.filepath}") from e

        source_fps = float(metadata['fps'])

        # Count source frames.
        total_source_frames = 0
        for _ in iio.imiter(self.filepath):
            total_source_frames += 1

        source_duration = total_source_frames / source_fps      # in seconds

        total_target_frames = int(source_duration * self.fps)
        frame_duration = source_duration / total_target_frames  # in seconds

        # Set up video display
        if self.show_img:
            try:
                import matplotlib.pyplot as plt

                preview_im = None
                plt.ion()
                fig, ax = plt.subplots()
                ax.axis('off')
                fig.canvas.manager.set_window_title('Processing video...')
            except ImportError as e:
                raise ImportError("Set show_img to False or install 'show_img' extras: matplotlib") from e

        processed_frames = []

        frame_step = source_fps / self.fps
        next_source_frame = 0

        for source_frame_idx, frame_rgb in enumerate(iio.imiter(self.filepath)):

            # Skip frames to achieve desired fps.
            if source_frame_idx < int(next_source_frame):
                continue
            next_source_frame += frame_step

            # Processing.
            frame_resized = np.asarray(
                Image.fromarray(frame_rgb).resize(
                    self.resolution,
                    Image.Resampling.BILINEAR
                )
            )

            data = frame_resized.astype(np.float32) / 255
            data_dithered = self.ditherer(data)
            data_avg = np.average(data_dithered[:, :, :3], axis=2, weights=np.asarray(self.channel_weights))
            pix_arr = np.where(data_avg >= self.threshold, 0, 1)

            processed_frames.append(pix_arr)

            if len(processed_frames) >= total_target_frames:
                break

            # Display video as it processes.
            if self.show_img:
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

        if self.show_img:
            plt.close(fig)

        return processed_frames, frame_duration
