from typing import Callable
import importlib.util

from .pixel_builder import Pixels
from .object import Object, CustomObject
from .dithering import floyd_steinberg

_default_show_img = importlib.util.find_spec('matplotlib') is not None


class CHImage(CustomObject):
    """circloO Helper Image"""

    def __init__(self,
                 filepath: str,
                 obj: Object,
                 downsample_factor: int,
                 threshold: int | float = .5,
                 channel_weights: tuple[int | float, int | float, int | float] = (1, 1, 1),
                 ditherer: Callable[['np.array'], 'np.array'] = floyd_steinberg,
                 show_img: bool | None = None):
        """
        Converts an image into circloO objects via dithering & grayscale conversion.
        Usage without dithering (using MoveableRectangles) is natively in the game using Ctrl+Shift+F4.
        :param filepath:            Path to input image
        :param obj:                 Object to be tiled into image. Top-left object of the image has obj's coordinates.
        :param downsample_factor:   Factor to downscale/downsample image; 1 for no change; should be higher for images with higher resolutions
        :param threshold:           Threshold for grayscale conversion; default is 0.5
        :param channel_weights:     Weights for RGB channels; default is (1, 1, 1)
        :param ditherer:            Dithering function (found in `dithering` module); default is floyd_steinberg
        :param show_img:            If True, displays the processed image; if None, default value is True when matplotlib is installed and False otherwise; default is None
        """
        super().__init__()

        self.filepath = filepath
        self.obj = obj
        self.downsample_factor = downsample_factor
        self.threshold = threshold
        self.channel_weights = channel_weights
        self.ditherer = ditherer
        self.show_img = show_img if show_img is not None else _default_show_img

    def _build_objs(self):
        super()._build_objs()

        try:
            import numpy as np
            from PIL import Image
        except ImportError as e:
            raise ImportError("Install 'image' extras: numpy, pillow") from e

        img = Image.open(self.filepath)

        data = np.asarray(img).astype(np.float32) / 255   # normalize values as floats b/w 0 & 1
        if len(data.shape) == 2:    # add new channel if B&W image to preserve algorithms
            data = data[:, :, np.newaxis]

        data_downsampled = data[::self.downsample_factor, ::self.downsample_factor, :]
        data_dithered = self.ditherer(data_downsampled)

        data_avg = np.average(data_dithered[:, :, :3], axis=2, weights=np.asarray(self.channel_weights))
        pix_arr = np.where(data_avg >= self.threshold, 0, 1)

        if self.show_img:
            try:
                import matplotlib.pyplot as plt
                plt.imshow(pix_arr, cmap='Greys')
                plt.show()
            except ImportError as e:
                raise ImportError("Set show_img to False or install 'show_img' extras: matplotlib") from e

        self._obj_cache.extend(Pixels(pix_arr, self.obj).get_objs())

        self._is_already_built = True
        return self._obj_cache
