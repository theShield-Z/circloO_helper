import numpy as _np
from .objects import Rectangle as _R

def build(arr: _np.array, start_x=1500, start_y=1500, size=1):
    """
    Convert image array into circloO objects.
    :param arr: Binary array
    :param start_x: Initial x value (left)
    :param start_y: Initial y value (top)
    :param size: Size of each pixel
    :return: String of circloO objects (w/o header)
    """

    objs = []

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == 1:
                xpos = j * 2 * size + start_x
                ypos = i * 2 * size + start_y
                objs.append(_R(xpos, ypos, size, size))

    return objs
