import math
import subprocess
from .level import Level
from .object import Object
import circloo_helper.object_shapes as _os
from .circloo_objects import Line, Arc, Curve, Dummy, Portal
from copy import copy

__all__ = ["polar", "pivot", "push_to_android", "combine"]


def polar(r, theta, start_x=1500, start_y=1500, in_degrees=True):
    """Converts a point in polar coordinates to rectangular coordinates."""
    if in_degrees:  # Angle given in degrees, convert to radians.
        theta = math.radians(theta)

    x = r * math.cos(theta)
    y = r * math.sin(theta)

    # Zero precision error (rounding).
    x = round(x, 4)
    y = round(y, 4)

    # Set to center.
    x += start_x
    y += start_y

    return x, y


def pivot(obj: Object, theta, pivot_x=1500, pivot_y=1500, in_degrees=True):
    """
    Rotate an Object or ObjectGroup around a pivot.
    :param obj:         Object to be rotated.
    :param theta:       Angle by which to rotate object.
    :param pivot_x:     X coordinate of pivot point.
    :param pivot_y:     Y coordinate of pivot point.
    :param in_degrees:  If True, assumes given angle theta is in degrees (instead of radians); default is True.
    """
    def pivot_single(x, y):
        """Pivots a single x/y point pair."""
        translated_x = x - pivot_x
        translated_y = y - pivot_y

        rotated_x = translated_x * math.cos(theta) - translated_y * math.sin(theta)
        rotated_y = translated_x * math.sin(theta) + translated_y * math.cos(theta)

        new_x = rotated_x + pivot_x
        new_y = rotated_y + pivot_y

        return new_x, new_y

    new_obj = copy(obj)

    if in_degrees:
        theta = math.radians(theta)

    if (isinstance(obj, _os.Circle)
            or isinstance(obj, _os.Player)
            or isinstance(obj, _os.Collectable)
            or isinstance(obj, Dummy)):
        new_x, new_y = pivot_single(obj.x, obj.y)
        new_obj.x = new_x
        new_obj.y = new_y

    elif isinstance(obj, _os.Rectangle):
        if obj.coords_by_center:
            new_x, new_y = pivot_single(obj.x, obj.y)

            new_obj.x = new_x
            new_obj.y = new_y
        else:
            half_w = obj.width / 2
            half_h = obj.height / 2

            new_x, new_y = pivot_single(obj.x + half_w, obj.y + half_h)

            new_obj.x = new_x - half_w
            new_obj.y = new_y - half_h

        new_rotation = obj.rotation + math.degrees(theta)
        new_obj.rotation = new_rotation

    elif isinstance(obj, _os.Triangle):
        new_x1, new_y1 = pivot_single(obj.x1, obj.y1)
        new_x2, new_y2 = pivot_single(obj.x2, obj.y2)
        new_x3, new_y3 = pivot_single(obj.x3, obj.y3)

        new_obj.x1 = new_x1
        new_obj.y1 = new_y1
        new_obj.x2 = new_x2
        new_obj.y2 = new_y2
        new_obj.x3 = new_x3
        new_obj.y3 = new_y3

    elif isinstance(obj, Line):
        new_x1, new_y1 = pivot_single(obj.x1, obj.y1)
        new_x2, new_y2 = pivot_single(obj.x2, obj.y2)

        new_obj.x1 = new_x1
        new_obj.y1 = new_y1
        new_obj.x2 = new_x2
        new_obj.y2 = new_y2

    elif isinstance(obj, Arc):
        new_x, new_y = pivot_single(obj.center_x, obj.center_y)
        new_cx, new_cy = pivot_single(obj.ctr_x, obj.ctr_y)
        new_start = obj.start_angle + math.degrees(theta)
        new_end = obj.end_angle + math.degrees(theta)

        new_obj.center_x = new_x
        new_obj.center_y = new_y
        new_obj.ctr_x = new_cx
        new_obj.ctr_y = new_cy
        new_obj.start_angle = new_start
        new_obj.end_angle = new_end

    elif isinstance(obj, Curve):
        new_sx, new_sy = pivot_single(obj.start_x, obj.start_y)
        new_c1x, new_c1y = pivot_single(obj.ctr1_x, obj.ctr1_y)
        new_c2x, new_c2y = pivot_single(obj.ctr2_x, obj.ctr2_y)
        new_ex, new_ey = pivot_single(obj.end_x, obj.end_y)

        new_obj.start_x = new_sx
        new_obj.start_y = new_sy
        new_obj.ctr1_x = new_c1x
        new_obj.ctr1_y = new_c1y
        new_obj.ctr2_x = new_c2x
        new_obj.ctr2_y = new_c2y
        new_obj.end_x = new_ex
        new_obj.end_y = new_ey

    elif isinstance(obj, Portal):
        new_x, new_y = pivot_single(obj.portal_x, obj.portal_y)
        new_obj.portal_x = new_x
        new_obj.portal_y = new_y

    else:
        # Object cannot be pivoted, a simple shallow copy will be returned.
        pass

    return new_obj


def push_to_android(file_path, destination='/sdcard'):
    """
    Pushes a file to an Android device using ADB.
    """
    try:
        command = ['adb', 'push', file_path, destination]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"File successfully pushed to {destination} folder.")
        else:
            print(f"Error pushing file: {result.stderr}")
    except Exception as e:
        print(f"An error has occurred: {e}")


def combine(level_1: Level, level_2: Level) -> Level:
    """
    Combines the contents of two levels, keeping the header of the first level and ensuring no duplicates.
    """
    new_level = copy(level_1)
    for obj in level_2.get_objs():
        if obj not in new_level.get_objs():
            new_level.add(obj)
    return new_level
