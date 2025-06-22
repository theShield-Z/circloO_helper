import math
import math as _math
import subprocess as _subprocess
from .level import Level as _Level
from .object import Object as _Object
# from .object_groups import ObjectGroup as _ObjectGroup
from .objects import Rectangle, Arc

__all__ = ["polar", "pivot", "push_to_android", "combine"]


def polar(r, theta, start_x=1500, start_y=1500, in_degrees=True):
    """Converts a point in polar coordinates to rectangular coordinates."""
    if in_degrees:  # Angle given in degrees, convert to radians.
        theta = _math.radians(theta)

    x = r * _math.cos(theta)
    y = r * _math.sin(theta)

    # Zero precision error.
    if abs(x) < 0.000001:
        x = 0.0
    if abs(y) < 0.000001:
        y = 0.0

    # Set to center.
    x += start_x
    y += start_y

    return (x, y)


def pivot(obj: _Object | list[_Object], theta, pivot_x=1500, pivot_y=1500, in_degrees=True):
    """
    Rotate an Object around a pivot.
    :param obj:         Object to be rotated.
    :param theta:       Angle by which to rotate object.
    :param pivot_x:     X coordinate of pivot point.
    :param pivot_y:     Y coordinate of pivot point.
    :param in_degrees:  If True, assumes given angle theta is in degrees (instead of radians); default is True.
    """

    # should probable change this to return a pivoted obj, not change the input obj

    if isinstance(obj, _Object):
        num = obj.number_of_positions

        if in_degrees:
            theta = math.radians(theta)

        if num <= 0:
            return

        # Initialize positions to add (obj.set_position() ignores None values)
        new_pos = [None, None, None, None]

        for i, pos in enumerate(obj.get_position()):
            # Loop through each of object's position points.
            init_x = pos[0]
            init_y = pos[1]

            # Translate to origin.
            translated_x = init_x - pivot_x
            translated_y = init_y - pivot_y

            # Apply standard rotation formula.
            rotated_x = translated_x * math.cos(theta) - translated_y * math.sin(theta)
            rotated_y = translated_x * math.sin(theta) + translated_y * math.cos(theta)

            # Translate back to pivot point.
            new_x = rotated_x + pivot_x
            new_y = rotated_y + pivot_y

            try:
                new_pos[i] = (new_x, new_y)
            except IndexError:
                raise IndexError("Apparently there's now an object with more than 4 positions??? Fix this, future me: tools.pivot()")

        if isinstance(obj, Rectangle):
            # Change rotation angle
            pass

        elif isinstance(obj, Arc):
            # Change start & end angles
            pass

        obj.set_position(*new_pos)

    elif isinstance(obj, list):

        # Is Group of Objects; loop through each object in group and apply pivot algorithm.
        for item in obj:
            pivot(item, theta, pivot_x, pivot_y, in_degrees)


def push_to_android(file_path, destination='/sdcard'):
    """
    Pushes a file to an Android device using ADB.
    """
    try:
        command = ['adb', 'push', file_path, destination]

        result = _subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"File successfully pushed to {destination} folder.")
        else:
            print(f"Error pushing file: {result.stderr}")
    except Exception as e:
        print(f"An error has occurred: {e}")


def combine(level_1: _Level, level_2: _Level) -> _Level:
    """
    Combines the objects of two levels, keeping the header of the first level.
    """
    new_level = level_1.copy()
    new_level.add(level_2.objs)
    return new_level
