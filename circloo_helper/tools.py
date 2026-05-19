import math
import subprocess
from copy import copy

from .object import Object
import circloo_helper.object_shapes as _os
from .circloo_objects import Line, Arc, Curve, Dummy, Portal

__all__ = ["polar", "pivot", "translate", "scale", "dimensions", "centroid", "push_to_android", "combine"]


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
    Rotate an Object around a pivot.
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


def translate(obj: Object, by_x=0, by_y=0):
    """
    Translate an Object by x and y.
    :param obj:     Object to be rotated.
    :param by_x:    Number of units to be translated along the x-axis
    :param by_y:    Number of units to be translated along the y-axis
    """
    def translate_single(x, y):
        """Translates a single x/y point pair."""
        return x + by_x, y + by_y

    new_obj = copy(obj)

    if (isinstance(obj, _os.Circle)
            or isinstance(obj, _os.Player)
            or isinstance(obj, _os.Collectable)
            or isinstance(obj, Dummy)):
        new_x, new_y = translate_single(obj.x, obj.y)
        new_obj.x = new_x
        new_obj.y = new_y

    elif isinstance(obj, _os.Rectangle):
        if obj.coords_by_center:
            new_x, new_y = translate_single(obj.x, obj.y)

            new_obj.x = new_x
            new_obj.y = new_y
        else:
            half_w = obj.width / 2
            half_h = obj.height / 2

            new_x, new_y = translate_single(obj.x + half_w, obj.y + half_h)

            new_obj.x = new_x - half_w
            new_obj.y = new_y - half_h

    elif isinstance(obj, _os.Triangle):
        new_x1, new_y1 = translate_single(obj.x1, obj.y1)
        new_x2, new_y2 = translate_single(obj.x2, obj.y2)
        new_x3, new_y3 = translate_single(obj.x3, obj.y3)

        new_obj.x1 = new_x1
        new_obj.y1 = new_y1
        new_obj.x2 = new_x2
        new_obj.y2 = new_y2
        new_obj.x3 = new_x3
        new_obj.y3 = new_y3

    elif isinstance(obj, Line):
        new_x1, new_y1 = translate_single(obj.x1, obj.y1)
        new_x2, new_y2 = translate_single(obj.x2, obj.y2)

        new_obj.x1 = new_x1
        new_obj.y1 = new_y1
        new_obj.x2 = new_x2
        new_obj.y2 = new_y2

    elif isinstance(obj, Arc):
        new_x, new_y = translate_single(obj.center_x, obj.center_y)
        # new_cx, new_cy = translate_single(obj.ctr_x, obj.ctr_y)

        new_obj.center_x = new_x
        new_obj.center_y = new_y
        # new_obj.ctr_x = new_cx
        # new_obj.ctr_y = new_cy

    elif isinstance(obj, Curve):
        new_sx, new_sy = translate_single(obj.start_x, obj.start_y)
        new_c1x, new_c1y = translate_single(obj.ctr1_x, obj.ctr1_y)
        new_c2x, new_c2y = translate_single(obj.ctr2_x, obj.ctr2_y)
        new_ex, new_ey = translate_single(obj.end_x, obj.end_y)

        new_obj.start_x = new_sx
        new_obj.start_y = new_sy
        new_obj.ctr1_x = new_c1x
        new_obj.ctr1_y = new_c1y
        new_obj.ctr2_x = new_c2x
        new_obj.ctr2_y = new_c2y
        new_obj.end_x = new_ex
        new_obj.end_y = new_ey

    elif isinstance(obj, Portal):
        new_x, new_y = translate_single(obj.portal_x, obj.portal_y)
        new_obj.portal_x = new_x
        new_obj.portal_y = new_y

    else:
        # Object cannot be translated, a simple shallow copy will be returned.
        pass

    return new_obj


def scale(obj: Object, by_x, by_y=None):
    """
    Scale an Object by x and y, originated from the centroid of the Object.
    :param obj:     Object to be rotated.
    :param by_x:    Number of units to be scaled along the x-axis
    :param by_y:    Number of units to be scaled along the y-axis. If None, by_x is used for both axes.
    """
    if by_x == 0 or by_y == 0:
        raise ValueError("Cannot scale an object by 0.")

    if by_y is None:
        by_y = by_x

    new_obj = copy(obj)

    if isinstance(obj, _os.Player):
        new_obj.size *= by_x

    elif isinstance(obj, _os.Circle):
        new_obj.radius *= by_x

    elif isinstance(obj, _os.Rectangle):
        new_obj.x -= obj.width / 2
        new_obj.y -= obj.height / 2
        new_obj.width *= by_x
        new_obj.height *= by_y

    elif isinstance(obj, _os.Triangle):
        cx = (obj.x1 + obj.x2 + obj.x3) / 3
        cy = (obj.y1 + obj.y2 + obj.y3) / 3

        new_x1 = cx + (obj.x1 - cx) * by_x
        new_y1 = cy + (obj.y1 - cy) * by_y
        new_x2 = cx + (obj.x2 - cx) * by_x
        new_y2 = cy + (obj.y2 - cy) * by_y
        new_x3 = cx + (obj.x3 - cx) * by_x
        new_y3 = cy + (obj.y3 - cy) * by_y

        new_obj.x1 = new_x1
        new_obj.y1 = new_y1
        new_obj.x2 = new_x2
        new_obj.y2 = new_y2
        new_obj.x3 = new_x3
        new_obj.y3 = new_y3

    elif isinstance(obj, Line):
        cx = (obj.x1 + obj.x2) / 2
        cy = (obj.y1 + obj.y2) / 2

        new_x1 = cx + (obj.x1 - cx) * by_x
        new_y1 = cy + (obj.y1 - cy) * by_y
        new_x2 = cx + (obj.x2 - cx) * by_x
        new_y2 = cy + (obj.y2 - cy) * by_y

        new_obj.x1 = new_x1
        new_obj.y1 = new_y1
        new_obj.x2 = new_x2
        new_obj.y2 = new_y2

        new_obj.thickness *= (by_x + by_y) / 2

    elif isinstance(obj, Arc):
        new_obj.radius *= by_x
        new_obj.thickness *= (by_x + by_y) / 2

    elif isinstance(obj, Curve):
        cx = (obj.start_x + obj.ctr1_x + obj.ctr2_x + obj.end_x) / 4
        cy = (obj.start_y + obj.ctr1_y + obj.ctr2_y + obj.end_y) / 4

        new_start_x = cx + (obj.start_x - cx) * by_x
        new_start_y = cy + (obj.start_y - cy) * by_y
        new_ctr1_x = cx + (obj.ctr1_x - cx) * by_x
        new_ctr1_y = cy + (obj.ctr1_y - cy) * by_y
        new_ctr2_x = cx + (obj.ctr2_x - cx) * by_x
        new_ctr2_y = cy + (obj.ctr2_y - cy) * by_y
        new_end_x = cx + (obj.end_x - cx) * by_x
        new_end_y = cy + (obj.end_y - cy) * by_y

        new_obj.start_x = new_start_x
        new_obj.start_y = new_start_y
        new_obj.ctr1_x = new_ctr1_x
        new_obj.ctr1_y = new_ctr1_y
        new_obj.ctr2_x = new_ctr2_x
        new_obj.ctr2_y = new_ctr2_y
        new_obj.end_x = new_end_x
        new_obj.end_y = new_end_y

        new_obj.thickness *= (by_x + by_y) / 2

    else:
        # Object cannot be scaled, a simple shallow copy will be returned.
        pass

    return new_obj


def dimensions(obj: Object):
    """Return the dimensions of an Object's bounding box as (width, height)."""
    if isinstance(obj, _os.Connection):
        raise TypeError("Connections have no dimensions.")

    if isinstance(obj, _os.Circle):
        width = height = obj.radius * 2 + 1     # actual circle radius is .5 greater than written radius
    elif isinstance(obj, Arc):
        ### TODO: possibly alter this for the minimum circumrectangle for the given start/end angles
        width = height = (obj.radius + obj.thickness) * 2
    elif isinstance(obj, _os.Rectangle):
        width = obj.width
        height = obj.height
    elif isinstance(obj, _os.Triangle):
        width = max(obj.x1, obj.x2, obj.x3) - min(obj.x1, obj.x2, obj.x3)
        height = max(obj.y1, obj.y2, obj.y3) - min(obj.y1, obj.y2, obj.y3)
    elif isinstance(obj, Line):
        width = max(obj.x1, obj.x2) - min(obj.x1, obj.x2)
        height = max(obj.y1, obj.y2) - min(obj.y1, obj.y2)
        if width == 0:
            width = obj.thickness * 2
        if height == 0:
            height = obj.thickness * 2
    elif isinstance(obj, Curve):
        ### TODO: scale as bounding box (circumrectangle) of curve
        width = abs(obj.start_x - obj.end_x)
        height = abs(obj.start_y - obj.end_y)
    elif isinstance(obj, _os.Collectable):
        width = height = 50
    elif isinstance(obj, Portal):
        width = height = 40.5
    elif isinstance(obj, _os.Player):
        width = height = obj.size * 64 + 1
    else:
        raise TypeError(f"Object {type(obj)} has no dimensions.")
    return width, height


def centroid(obj: Object):
    """Return the (x, y) coordinate of an Object's centroid (geometric center)."""

    if (isinstance(obj, _os.Circle)
            or isinstance(obj, _os.Player)
            or isinstance(obj, _os.Collectable)
            or isinstance(obj, Dummy)):
        cx = obj.x
        cy = obj.y

    elif isinstance(obj, _os.Rectangle):
        cx = obj.x + obj.width / 2
        cy = obj.y + obj.height / 2

    elif isinstance(obj, _os.Triangle):
        cx = (obj.x1 + obj.x2 + obj.x3) / 3
        cy = (obj.y1 + obj.y2 + obj.y3) / 3

    elif isinstance(obj, Line):
        cx = (obj.x1 + obj.x2) / 2
        cy = (obj.y1 + obj.y2) / 2

    elif isinstance(obj, Arc):
        cx = obj.center_x
        cy = obj.center_y

    elif isinstance(obj, Curve):
        cx = (obj.start_x + obj.ctr1_x + obj.ctr2_x + obj.end_x) / 4
        cy = (obj.start_y + obj.ctr1_y + obj.ctr2_y + obj.end_y) / 4

    elif isinstance(obj, Portal):
        cx = obj.portal_x
        cy = obj.portal_y

    else:
        raise TypeError(f"Object {type(obj)} does not have a centroid.")

    return cx, cy


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


def combine(level_1: 'Level', level_2: 'Level') -> 'Level':
    """
    Combines the contents of two levels, keeping the header of the first level and ensuring no duplicates.
    """
    new_level = copy(level_1)
    for obj in level_2.get_objs():
        if obj not in new_level.get_objs():
            new_level.add(obj)
    return new_level
