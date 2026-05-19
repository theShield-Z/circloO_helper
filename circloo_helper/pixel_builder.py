import numpy as np
from copy import copy

from .object import CustomObject, Object
from .tools import translate, dimensions
import circloo_helper.object_shapes as _os


class Pixels(CustomObject):
    def __init__(self,
                 arr: np.array,
                 obj: Object,
                 scale_x: float | int | None = None,
                 scale_y: float | int | None = None,
                 reduce_rectangles: bool = True):
        """
        Tiles an input Object according to an input 2D binary array.
        :param arr:         2D binary array. Object is created in each cell with a 1, 0's are ignored
        :param obj:         Object to be tiled. Pixel array starts at obj coordinates.
        :param scale_x:     Distance between each object (x). If None, value is the width of obj. Default is None.
        :param scale_y:     Distance between each object (y). If None, value is the height of obj. Default is None.
        :param reduce_rectangles:   If True and obj is a Rectangle, pixel array is built with greedy rectangle
                                    decomposition to reduce object count. Default is True.
        """
        super().__init__()

        self.arr = np.asarray(arr)
        self.obj: Object = obj

        self.reduce_rectangles = reduce_rectangles

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

        if self.reduce_rectangles and isinstance(self.obj, _os.Rectangle):
            return self._reduced_build()

        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j] == 1:
                    x = j * self.scale_x
                    y = i * self.scale_y
                    self._obj_cache.append(translate(self.obj, x, y))

        return self._obj_cache

    def _reduced_build(self):
        """Build the pixel array using greedy rectangle decomposition to reduce object count."""
        if not isinstance(self.obj, _os.Rectangle):
            raise TypeError("Cannot use greedy rectangle decomposition on non-Rectangles.")

        arr = self.arr

        # Build reduction matrix.

        red_mat = np.zeros((*arr.shape, 2))

        for i in range(len(arr)):
            point_hor = None

            for j in range(len(arr[i])):
                cur = arr[i, j]

                if cur == 1:
                    if point_hor is None:
                        point_hor = (i, j, 0)
                        red_mat[point_hor] = 1
                    else:
                        red_mat[point_hor] += 1

                else:
                    point_hor = None

        for j in range(len(arr[0])):
            point_vert = None

            for i in range(len(arr)):
                cur = red_mat[i, j, 0]

                if cur > 0:
                    if point_vert is None:
                        point_vert = (i, j)
                        red_mat[(*point_vert, 1)] = 1
                    else:
                        if cur == red_mat[(*point_vert, 0)]:
                            red_mat[(*point_vert, 1)] += 1
                            red_mat[i, j, 0] = 0
                        else:
                            point_vert = (i, j)
                            red_mat[(*point_vert, 1)] = 1
                else:
                    point_vert = None

        # Print reduction matrix (debug)
        # for i in range(len(red_mat)):
        #     for j in range(len(red_mat[i])):
        #         print("(", end='')
        #         for k in range(len(red_mat[i][j])):
        #             # print(red_mat[i][j][k], ' ', end='')
        #             print(f"{red_mat[i][j][k]}, ", end='')
        #         print(") ", end='')
        #     print()

        # Build object cache.

        for i in range(len(red_mat)):
            for j in range(len(red_mat[i])):
                if all(red_mat[i, j] > 0):
                    x = j * self.scale_x
                    y = i * self.scale_y
                    new_obj = copy(self.obj)
                    new_obj.width *= red_mat[i, j, 0]
                    new_obj.height *= red_mat[i, j, 1]
                    self._obj_cache.append(translate(new_obj, x, y))

        return self._obj_cache
