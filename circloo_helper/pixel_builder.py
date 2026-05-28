import numpy as np
import numba

from .object import CustomObject, Object
from .tools import translate, dimensions
from .object_shapes import Rectangle
from .object_types import Generator


class Pixels(CustomObject):
    def __init__(self,
                 arr: np.array,
                 obj: Object,
                 scale_x: float | int | None = None,
                 scale_y: float | int | None = None,
                 reduce_objects: bool = True):
        """
        Tiles an input Object according to an input 2D or 3D binary array.
        :param arr:         2D or 3D binary array. Object is created in each cell with a 1, 0's are ignored.
                                If 3D, third dimension is time (only usable for Generator type objects)
        :param obj:         Object to be tiled. Pixel array starts at obj coordinates.
        :param scale_x:     Distance between each object (x). If None, value is the width of obj. Default is None.
        :param scale_y:     Distance between each object (y). If None, value is the height of obj. Default is None.
        :param reduce_objects:   If True, multiple object reduction steps will be taken. I highly discourage setting
                                    this to False. For Rectangle objects, greedy rectangle decomposition will be
                                    performed. For 3D arrays, Generators that are on for multiple frames will be merged
                                    into a single Generator that stays on during all frames.
        """
        super().__init__()

        self.arr = np.asarray(arr)
        self.obj: Object = obj

        self.reduce_rectangles = reduce_objects

        if scale_x is not None:
            self.scale_x = scale_x
            self._is_manually_scaled_x = True
            self.reduce_rectangles = False  # Cannot merge rects if they are not touching
        else:
            self.scale_x = None
            self._is_manually_scaled_x = False

        if scale_y is not None:
            self.scale_y = scale_y
            self._is_manually_scaled_y = True
            self.reduce_rectangles = False
        else:
            self.scale_y = None
            self._is_manually_scaled_y = False

    def _update_scale(self):
        scale_x, scale_y = dimensions(self.obj)

        if not self._is_manually_scaled_x:
            self.scale_x = scale_x
        if not self._is_manually_scaled_y:
            self.scale_y = scale_y

    def build_objs(self):
        super().build_objs()
        self._update_scale()

        if len(self.arr.shape) == 2:
            return self._build_2d()

        elif len(self.arr.shape) == 3:
            return self._build_3d()

        else:
            raise ValueError("Pixel array must be either 2D or 3D")

    def _build_2d(self):
        if self.reduce_rectangles and isinstance(self.obj, Rectangle):
            rects = self._rectangle_decomposer_2d(self.arr)
            for rect in rects:
                (x, y), (width, height) = rect

                obj = translate(self.obj, x * self.scale_x, y * self.scale_y)
                obj.width *= width
                obj.height *= height

                self._obj_cache.append(obj)

        else:
            for i in range(len(self.arr)):
                for j in range(len(self.arr[i])):
                    if self.arr[i][j] == 1:
                        x = j * self.scale_x
                        y = i * self.scale_y
                        self._obj_cache.append(translate(self.obj, x, y))

        return self._obj_cache

    def _build_3d(self):

        if not isinstance(self.obj, Generator):
            raise TypeError("Can only build a 3D pixel array with circloO Generator objects")

        if self.reduce_rectangles:

            if isinstance(self.obj, Rectangle):
                rects = self._rectangle_decomposer_3d(self.arr)
                for rect in rects:
                    (x, y, f), (width, height, duration) = rect

                    obj = translate(self.obj, x * self.scale_x, y * self.scale_y)
                    obj.width *= width
                    obj.height *= height
                    obj.init_delay += f * obj.disappear_after
                    obj.disappear_after *= duration
                    obj.wait_between = 9999

                    self._obj_cache.append(obj)

            else:
                # Reduce depth/duration only.
                #       This is the same algorithm as _rectangle_decomposer_3d, but only applied depth-wise.
                arr = self.arr.copy()
                a, b, c = arr.shape
                for j in range(b):
                    for k in range(c):
                        for i in range(a):

                            cur = arr[i, j, k]

                            if cur == 0:
                                continue

                            depth = 1
                            while i + depth < a and arr[i + depth, j, k] > 0:
                                depth += 1

                            obj = translate(self.obj, k * self.scale_x, j * self.scale_y)
                            obj.init_delay += i * obj.disappear_after
                            obj.disappear_after *= depth
                            obj.wait_between = 9999

                            self._obj_cache.append(obj)

                            arr[i: i + depth, j, k] = 0

        else:
            # No reductions.
            a, b, c = self.arr.shape
            for j in range(b):
                for k in range(c):
                    for i in range(a):
                        if self.arr[i][j][k] == 1:
                            obj = translate(self.obj, k * self.scale_x, j * self.scale_y)
                            obj.init_delay += i * obj.disappear_after
                            obj.wait_between = 9999

                            self._obj_cache.append(obj)

        return self._obj_cache

    @staticmethod
    @numba.njit
    def _rectangle_decomposer_2d(arr: np.array):
        """
        Decomposes a 2D numpy binary array into the minimum number of spanning rectangles
            using a width->height greedy algorithm
        :return: Generator that yields each rectangle as ((x, y), (width, height))
        """
        arr = arr.copy()
        b, c = arr.shape
        # b -> height of frame
        # c -> width of frame

        for j in range(b):
            for k in range(c):
                cur = arr[j, k]

                if cur == 0:
                    continue

                # Find width.
                width = 1
                while k + width < c:
                    if np.all(arr[j, k + width]):
                        width += 1
                    else:
                        break

                # Find height.
                height = 1
                while j + height < b:
                    if np.all(arr[j + height, k:k + width]):
                        height += 1
                    else:
                        break

                yield (k, j), (width, height)

                # Clear the determined region so that it is not processed again.
                arr[j: j + height, k: k + width] = 0

    @staticmethod
    @numba.njit
    def _rectangle_decomposer_3d(arr: np.array):
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
