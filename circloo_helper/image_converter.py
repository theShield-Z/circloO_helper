import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import numba

from .pixel_builder import Pixels
from .object import Object, CustomObject


class CHImage(CustomObject):
    """circloO Helper Image"""

    def __init__(self,
                 filepath: str,
                 obj: Object,
                 downsample_factor: int,
                 threshold: int = .5,
                 channel_weights: tuple[int | float, int | float, int | float] = (1, 1, 1),
                 show_img: bool = True):
        """
        Converts an image into circloO objects via dithering & grayscale conversion.
        Usage without dithering (using MoveableRectangles) is natively in the game using Ctrl+Shift+F4.
        :param filepath:            Path to input image
        :param obj:                 Object to be tiled into image. Top-left object of the image has obj's coordinates.
        :param downsample_factor:   Factor to downscale/downsample image; 1 for no change; should be higher for images with higher resolutions
        :param threshold:           Threshold for grayscale conversion; default is 0.5
        :param show_img:            If True, displays the processed image; default is True
        :param channel_weights:     Weights for RGB channels; default is (1, 1, 1)
        """
        super().__init__()

        self._img = Image.open(filepath)
        self._obj = obj
        self._downsample_factor = downsample_factor
        self._show_img = show_img
        self._threshold = threshold
        self._channel_weights = channel_weights

        self._is_already_built = False

    def build_objs(self):
        if self._is_already_built:
            return self._obj_cache

        super().build_objs()

        data = np.asarray(self._img).astype(np.float32) / 255   # normalize values as floats b/w 0 & 1
        if len(data.shape) == 2:    # add new channel if B&W image to preserve algorithms
            data = data[:, :, np.newaxis]

        data_downsampled = data[::self._downsample_factor, ::self._downsample_factor, :]
        data_dithered = self.floyd_steinberg(data_downsampled)  # note if it ever becomes an issue: this changes data_downsampled too

        data_avg = np.average(data_dithered[:, :, :3], axis=2, weights=np.asarray(self._channel_weights))
        pix_arr = np.where(data_avg >= self._threshold, 0, 1)

        if self._show_img:
            plt.imshow(pix_arr, cmap='Greys')
            plt.show()

        self._obj_cache.extend(Pixels(pix_arr, self._obj).build_objs())

        self._is_already_built = True
        return self._obj_cache

    @staticmethod
    @numba.jit
    def floyd_steinberg(image: np.array):
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
