import math
import subprocess
from copy import copy
from warnings import warn
from functools import cache

from .object import Object, CustomObject
import circloo_helper.object_shapes as _os
from .circloo_objects import Line, Arc, Curve, Dummy, Portal
from .level import Level as Level

__all__ = ["polar",
           "pivot", "translate", "scale",
           "bounding_box", "dimensions", "centroid",
           "push_to_android", "combine"]


class _TransformObject(CustomObject):
    """
    A simple wrapper of a CustomObject's object cache (returned from get_objs()) to provide CustomObject functionality to the list.
    Created when using transformation tools on a CustomObject.
    """
    def __init__(self, objs: list = None):
        super().__init__()
        self.objs = objs if objs is not None else []

    def _build_objs(self):
        super()._build_objs()
        self._obj_cache = self.objs
        return self._obj_cache


def _rebind_connection_refs(obj, mapping):
    """Update connection endpoints to point at transformed children."""
    for attr in ("obj1", "obj2"):
        if hasattr(obj, attr):
            target = getattr(obj, attr, None)
            if target is not None and target in mapping:
                setattr(obj, attr, mapping[target])


def _get_curve_bbox(obj: Curve):
    """Returns bounding box as (xmin, xmax, ymin, ymax)"""
    try:
        from svgpathtools import CubicBezier
        p0 = complex(obj.start_x, obj.start_y)
        p1 = complex(obj.ctr1_x, obj.ctr1_y)
        p2 = complex(obj.ctr2_x, obj.ctr2_y)
        p3 = complex(obj.end_x, obj.end_y)
        return CubicBezier(p0, p1, p2, p3).bbox()
    except ImportError:
        # TODO: Implement custom implementation of CubicBezier.bbox() and remove svgpathtools dependency
        warn("tools.dimensions() or tools.centroid(): Inaccurate Curve bounding box. Install 'svg' extras for accurate calculations: svgpathtools-light")
        xmin = min(obj.start_x, obj.end_x, obj.ctr1_x, obj.ctr2_x)
        xmax = max(obj.start_x, obj.end_x, obj.ctr1_x, obj.ctr2_x)
        ymin = min(obj.start_y, obj.end_y, obj.ctr1_y, obj.ctr2_y)
        ymax = max(obj.start_y, obj.end_y, obj.ctr1_y, obj.ctr2_y)
        return xmin, xmax, ymin, ymax


def _get_arc_bbox(obj: Arc):
    """Returns bounding box as (xmin, xmax, ymin, ymax)"""

    start = math.radians(obj.start_angle)
    end = math.radians(obj.end_angle)
    tau = math.tau

    # Normalize so end >= start
    while end < start:
        end += tau

    # Candidate angles (endpoints & cardinal directions)
    candidate_angles = [start, end]

    for angle in (0, tau / 4, tau / 2, 3 * tau / 4):
        a = angle
        while a < start:
            a += tau
        if a <= end:
            candidate_angles.append(a)

    xs = []
    ys = []

    for a in candidate_angles:
        xs.append(obj.center_x + obj.radius * math.cos(a))
        ys.append(obj.center_y + obj.radius * math.sin(a))

    return (
        min(xs),
        max(xs),
        min(ys),
        max(ys),
    )


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


def pivot(obj: Object | CustomObject, theta, pivot_x=1500, pivot_y=1500, in_degrees=True) -> Object | _TransformObject:
    """
    Rotate an Object around a pivot.
    :param obj:         Object to be rotated.
    :param theta:       Angle by which to rotate object.
    :param pivot_x:     X coordinate of pivot point.
    :param pivot_y:     Y coordinate of pivot point.
    :param in_degrees:  If True, assumes given angle theta is in degrees (instead of radians); default is True.
    """
    if isinstance(obj, CustomObject):
        tf_obj = _TransformObject()
        mapping = {}

        for item in copy(obj).get_objs():
            transformed_item = pivot(item, theta, pivot_x, pivot_y, in_degrees)
            mapping[item] = transformed_item
            tf_obj.objs.append(transformed_item)

        for item in tf_obj.objs:
            _rebind_connection_refs(item, mapping)

        return tf_obj

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


def translate(obj: Object | CustomObject, by_x=0, by_y=0) -> Object | _TransformObject:
    """
    Translate an Object by x and y.
    :param obj:     Object to be rotated.
    :param by_x:    Number of units to be translated along the x-axis
    :param by_y:    Number of units to be translated along the y-axis
    """
    if isinstance(obj, CustomObject):
        tf_obj = _TransformObject()
        mapping = {}

        for item in copy(obj).get_objs():
            transformed_item = translate(item, by_x, by_y)
            mapping[item] = transformed_item
            tf_obj.objs.append(transformed_item)

        for item in tf_obj.objs:
            _rebind_connection_refs(item, mapping)

        return tf_obj

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


def scale(obj: Object | CustomObject, by_x, by_y=None) -> Object | _TransformObject:
    """
    Scale an Object by x and y, originated from the centroid of the Object.
    :param obj:     Object to be rotated.
    :param by_x:    Number of units to be scaled along the x-axis
    :param by_y:    Number of units to be scaled along the y-axis. If None, by_x is used for both axes.
    """
    if isinstance(obj, CustomObject):
        # TODO: This should originate from the CustomObject's centroid, not each individual composing object.
        tf_obj = _TransformObject()
        mapping = {}

        for item in copy(obj).get_objs():
            transformed_item = scale(item, by_x, by_y)
            mapping[item] = transformed_item
            tf_obj.objs.append(transformed_item)

        for item in tf_obj.objs:
            _rebind_connection_refs(item, mapping)

        return tf_obj

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


@cache
def bounding_box(obj: Object | CustomObject) -> tuple[float | int, float | int, float | int, float | int]:
    """
    Return the coordinates of the bounding box of an Object or CustomObject as (xmin, xmax, ymin, ymax).
    """

    if isinstance(obj, CustomObject):
        xmin, xmax, ymin, ymax = float('inf'), -float('inf'), float('inf'), -float('inf')
        for item in copy(obj).get_objs():
            try:
                xmin_, xmax_, ymin_, ymax_ = bounding_box(item)
                if xmin_ < xmin:
                    xmin = xmin_
                if xmax_ > xmax:
                    xmax = xmax_
                if ymin_ < ymin:
                    ymin = ymin_
                if ymax_ > ymax:
                    ymax = ymax_

            except ValueError:
                continue

        if any([val in (float('inf'), -float('inf')) for val in [xmin, xmax, ymin, ymax]]):
            raise ValueError(f"Object does not have coordinates and cannot be given a bounding box: {[xmin, xmax, ymin, ymax]}")

        return xmin, xmax, ymin, ymax

    elif isinstance(obj, _os.Circle):
        return (obj.x - obj.radius - .5,
                obj.x + obj.radius + .5,
                obj.y - obj.radius - .5,
                obj.y + obj.radius + .5)

    elif isinstance(obj, _os.Rectangle):
        # Bounding boxes must account for rotation.

        angle = math.radians(obj.rotation)
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        hw = obj.width / 2
        hh = obj.height / 2

        if obj.coords_by_center:
            cx, cy = obj.x, obj.y
        else:
            cx = obj.x + hw
            cy = obj.y + hh

        rotated_corners = []
        for x, y in [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]:
            rotated_corners.append((cx + x * cos_a - y * sin_a,
                                    cy + x * sin_a + y * cos_a))

        xs = [x for x, _ in rotated_corners]
        ys = [y for _, y in rotated_corners]

        return min(xs), max(xs), min(ys), max(ys)

    elif isinstance(obj, _os.Triangle):
        return (min(obj.x1, obj.x2, obj.x3),
                max(obj.x1, obj.x2, obj.x3),
                min(obj.y1, obj.y2, obj.y3),
                max(obj.y1, obj.y2, obj.y3))

    elif isinstance(obj, Arc):
        return _get_arc_bbox(obj)

    elif isinstance(obj, Curve):
        return _get_curve_bbox(obj)

    elif isinstance(obj, Line):
        return (min(obj.x1, obj.x2),
                max(obj.x1, obj.x2),
                min(obj.y1, obj.y2),
                max(obj.y1, obj.y2))

    elif isinstance(obj, _os.Collectable):
        return (obj.x - 25, obj.x + 25,
                obj.y - 25, obj.y + 25)

    elif isinstance(obj, Portal):
        rad = 40.5 / 2
        return (obj.portal_x - rad, obj.portal_x + rad,
                obj.portal_x - rad, obj.portal_y + rad)

    elif isinstance(obj, _os.Player):
        rad = (obj.size * 64 + 1) / 2
        return (obj.x - rad, obj.x + rad,
                obj.y - rad, obj.y + rad)

    else:
        raise ValueError("Object does not have coordinates and cannot be given a bounding box.")


def dimensions(obj: Object | CustomObject) -> tuple[float | int, float | int]:
    """Return the dimensions of an Object's bounding box as (width, height)."""

    if isinstance(obj, _os.Circle):
        width = height = obj.radius * 2 + 1     # actual circle radius is .5 greater than written radius

    elif isinstance(obj, Line):
        xmin, xmax, ymin, ymax = bounding_box(obj)
        width = xmax - xmin
        height = ymax - ymin
        if width == 0:
            width = obj.thickness * 2
        if height == 0:
            height = obj.thickness * 2

    elif isinstance(obj, _os.Collectable):
        width = height = 50

    elif isinstance(obj, Portal):
        width = height = 40.5

    elif isinstance(obj, _os.Player):
        width = height = obj.size * 64 + 1

    else:
        xmin, xmax, ymin, ymax = bounding_box(obj)
        width = xmax - xmin
        height = ymax - ymin

    return width, height


def centroid(obj: Object | CustomObject) -> tuple[float | int, float | int]:
    """Return the (x, y) coordinate of an Object's centroid (geometric center)."""

    if (isinstance(obj, _os.Circle)
            or isinstance(obj, _os.Player)
            or isinstance(obj, _os.Collectable)
            or isinstance(obj, Dummy)):
        cx = obj.x
        cy = obj.y

    elif isinstance(obj, _os.Rectangle):
        if obj.coords_by_center:
            cx = obj.x
            cy = obj.y
        else:
            cx = obj.x + obj.width / 2
            cy = obj.y + obj.height / 2

    elif isinstance(obj, Line):
        cx = (obj.x1 + obj.x2) / 2
        cy = (obj.y1 + obj.y2) / 2

    elif isinstance(obj, Portal):
        cx = obj.portal_x
        cy = obj.portal_y

    else:
        xmin, xmax, ymin, ymax = bounding_box(obj)
        cx = (xmax + xmin) / 2
        cy = (ymax + ymin) / 2

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


def combine(level_1: Level, level_2: Level) -> Level:
    """
    Combines the contents of two levels, keeping the header of the first level and ensuring no duplicates.
    """
    new_level = copy(level_1)
    for obj in level_2.get_objs():
        if obj not in new_level.get_objs():
            new_level.add(obj)
    return new_level
