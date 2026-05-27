from typing import Callable
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from .pixel_builder import Pixels
from .object import Object, CustomObject
from .dithering import floyd_steinberg


class CHImage(CustomObject):
    """circloO Helper Image"""

    def __init__(self,
                 filepath: str,
                 obj: Object,
                 downsample_factor: int,
                 threshold: int | float = .5,
                 channel_weights: tuple[int | float, int | float, int | float] = (1, 1, 1),
                 ditherer: Callable[[np.array], np.array] = floyd_steinberg,
                 show_img: bool = True):
        """
        Converts an image into circloO objects via dithering & grayscale conversion.
        Usage without dithering (using MoveableRectangles) is natively in the game using Ctrl+Shift+F4.
        :param filepath:            Path to input image
        :param obj:                 Object to be tiled into image. Top-left object of the image has obj's coordinates.
        :param downsample_factor:   Factor to downscale/downsample image; 1 for no change; should be higher for images with higher resolutions
        :param threshold:           Threshold for grayscale conversion; default is 0.5
        :param channel_weights:     Weights for RGB channels; default is (1, 1, 1)
        :param ditherer:            Dithering function (found in `dithering` module); default is floyd_steinberg
        :param show_img:            If True, displays the processed image; default is True
        """
        super().__init__()

        self._img = Image.open(filepath)
        self._obj = obj
        self._downsample_factor = downsample_factor
        self._show_img = show_img
        self._threshold = threshold
        self._channel_weights = channel_weights
        self._ditherer = ditherer

        self._is_already_built = False

    def build_objs(self):
        if self._is_already_built:
            return self._obj_cache

        super().build_objs()

        data = np.asarray(self._img).astype(np.float32) / 255   # normalize values as floats b/w 0 & 1
        if len(data.shape) == 2:    # add new channel if B&W image to preserve algorithms
            data = data[:, :, np.newaxis]

        data_downsampled = data[::self._downsample_factor, ::self._downsample_factor, :]
        data_dithered = self._ditherer(data_downsampled)

        data_avg = np.average(data_dithered[:, :, :3], axis=2, weights=np.asarray(self._channel_weights))
        pix_arr = np.where(data_avg >= self._threshold, 0, 1)

        if self._show_img:
            plt.imshow(pix_arr, cmap='Greys')
            plt.show()

        self._obj_cache.extend(Pixels(pix_arr, self._obj).build_objs())

        self._is_already_built = True
        return self._obj_cache
