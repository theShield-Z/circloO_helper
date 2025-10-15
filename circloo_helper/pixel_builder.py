import numpy as _np
from .objects import Rectangle as _R
from .object import Object as _O


"""Need to update this to be able to use any object."""


# old version; slightly faster for default operation, but outdated for use with other objects
def build(arr: _np.array, start_x=1500, start_y=1500, size=1, obj_type="b", *args):
    """
    Convert a binary array into circloO objects.
    Old version of build_(); slightly faster for default operation, but does not handle use with other objects well.
    :param arr: Binary array
    :param start_x: Initial x value (left)
    :param start_y: Initial y value (top)
    :param size: Size of each pixel
    :param obj_type: Tag for type of object used to build array; default is 'b' for rectangle (box); see documentation (in objects.py) for each object's tag.
    :param args: If obj_type is not "rectangle", the extra parameters used for the object; see documentation of each object (in objects.py) for syntax.
    :return: String of circloO objects (w/o header)
    """

    objs = []
    # if obj_type != "b":
    #     # args = list(args)
    #     # args[0] = obj_type, 0, 0, size, *args[0]
    #     attributes = obj_type, 0, 0, size, *args[0]
    #     other_args = args[1:]

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == 1:
                xpos = j * size + start_x
                ypos = i * size + start_y
                if obj_type == "b":
                    objs.append(_R(xpos, ypos, size, size))
                else:
                    attributes = obj_type, xpos + size/2, ypos + size/2, size/2, *args[0]
                    objs.append(_O(list(attributes), list(args[1])))

    return objs


def build_(arr: _np.array, start_x=1500, start_y=1500, size=1,
           attributes=None, modifiers=None,):
    """
    Convert a binary array into circloO objects. Builds with basic Rectangles by default, but args can be used to build
    with other objects using the base Object (in object.py) syntax with the optional arguments attributes, modifiers,
    and connections.

    When using other objects, mark the indices that should be replaced with the x-position, y-position, and size with
    "X", "Y", and "S", respcetively. You can also indicate that the size or position's value should be added to or
    multiplied by a number using +[number] or *[number] (- and / also work) prefixed by a '%' in the string. e.g., to
    add 1 to the size and multiply the size by .5, the attribute at the desired index should be "S%+1%*.5".

    Note that for most Rectangles, the x- and y-positions should be subtracted by half the size and the size should be
    multiplied by .5 to work properly. (I may make it do this automatically in the future.)
        For example, to use this with a RectangleGenerator with size=10 (and generate only once without disappearing),
        set attributes=['tmb', "X%+-5", "Y%+-5", "S%*.5", "S%*.5", 0, 0, 0, 0, 0, 9999*60, 0]

    :param arr: Binary array
    :param start_x: Initial x value (left)
    :param start_y: Initial y value (top)
    :param size: Size of each pixel
    :param attributes: Optional attributes if using objects other than the basic Rectangle.
    :param modifiers: Optional modifiers if using objects other than the basic Rectangle.
    :return: String of circloO objects (w/o header)
    """

    if attributes is None:
        attributes = ['b', f"X%+{-size/2}", f"Y%+{-size/2}", "S%*.5", "S%*.5", 0]
    if modifiers is None:
        modifiers = []

    objs = []

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == 1:
                xpos = j * size + start_x
                ypos = i * size + start_y

                """example formatted string:
                "X%+2%*4"
                """

                temp_attrs = attributes.copy()
                for a in range(len(attributes)):
                    att = temp_attrs[a]
                    if isinstance(att, str):
                        if att.startswith("X"):
                            temp_attrs[a] = _format_str(att, xpos, size)
                        elif att.startswith("Y"):
                            temp_attrs[a] = _format_str(att, ypos, size)
                        elif att.startswith("S"):
                            temp_attrs[a] = _format_str(att, size, size)

                objs.append(_O(temp_attrs, modifiers))

    return objs


def _format_str(fstr: str, number, size):
    arguments = fstr.split("%")
    for arg in arguments:
        if arg.startswith("+"):
            number += float(arg[1:])
        elif arg.startswith("*"):
            number *= float(arg[1:])
        elif arg.startswith("-"):
            number -= float(arg[1:])
        elif arg.startswith("/"):
            number /= float(arg[1:])
    return number


# POSSIBLE CHANGE?
# def _format_str(fstr: str, number, size):
#     arguments = fstr.split("%")
#     for arg in arguments:
#         if arg.startswith("+"):
#             arg.replace("size", size)
#             number += float(arg[1:])
#
#         elif arg.startswith("*"):
#             arg.replace("size", size)
#             number *= float(arg[1:])
#
#     return number

