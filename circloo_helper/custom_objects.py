import math as _math
import tripy

from .object import CustomObject as _CustomObject
from .tools import pivot as _pivot
import circloo_helper.circloo_objects as _o
import circloo_helper.object_types as _ot
import circloo_helper.object_shapes as _os


class OutlineRectangle(_CustomObject, _ot.Solid, _os.Rectangle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 width: int | float,
                 height: int | float,
                 rotation: int | float = 0,
                 thickness: int | float = 3,
                 coords_by_center: bool = False):
        """
        Solid outline of a Rectangle. Outline is along the inner edge.
        :param x_pos:       Position of top-left corner of rectangle (left), or of center if coords_by_center
        :param y_pos:       Position of top-left corner of rectangle (top), or of center if coords_by_center
        :param width:       Width of Rectangle
        :param height:      Height of Rectangle
        :param rotation:    Rotation of rectangle; increase to rotate clockwise; default is 0
        :param thickness:   Thickness of outline
        :param coords_by_center:    If True, interprets given position and size as from center; default is False.
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rotation = rotation
        self.thickness = thickness
        self.coords_by_center = coords_by_center

    def build_objs(self):
        super().build_objs()
        obj_cache = list()

        if self.coords_by_center:
            x_pos = self.x - (self.width / 2)
            y_pos = self.y - (self.height / 2)
        else:
            x_pos = self.x
            y_pos = self.y

        # TOP
        obj_cache.append(_o.SolidRectangle(x_pos, y_pos, self.width, self.thickness))

        # LEFT
        obj_cache.append(_o.SolidRectangle(x_pos, y_pos, self.thickness, self.height))

        # RIGHT
        obj_cache.append(_o.SolidRectangle(x_pos + self.width - self.thickness, y_pos, self.thickness, self.height))

        # BOTTOM
        obj_cache.append(_o.SolidRectangle(x_pos, y_pos + self.height - self.thickness, self.width, self.thickness))

        if self.rotation != 0:
            for obj in obj_cache:
                self._obj_cache.append(_pivot(obj, self.rotation, self.x, self.y))
        else:
            self._obj_cache.extend(obj_cache)

        return self._obj_cache


class MoveableArc(_CustomObject, _ot.Moveable, _os.Line):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 radius: int | float,
                 start_angle: int | float = 0,
                 end_angle: int | float = 360,
                 thickness: int | float = 3,
                 resolution: int | None = None,
                 density: int | float = 1,
                 damping: int | float = -1,
                 fix_rotation: bool = False,
                 bullet: bool = False):
        """
        Moveable Arc. Outline is centered on the radius.
        :param x_pos:           Position of center
        :param y_pos:           Position of center
        :param radius:          Radius of Arc
        :param start_angle:     Starting angle in degrees; default is 0 (full circle)
        :param end_angle:       Ending angle in degrees; default is ~360 (full circle)
        :param thickness:       Thickness of outline; default is 3
        :param resolution:      Number of rectangles the final arc is made up of; if None, calculates automatically; default is None
        :param density:         Density of arc; make 0 to turn solid; default is 1
        :param damping:         How quickly the object is slowed when no force is applied; default is 0
        :param fix_rotation:    Disable rotation if True; default is False
        :param bullet:          If True, enables setting to improve high-speed physics; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.thickness = thickness
        self.resolution = resolution

        self.density = density
        self.damping = damping
        self.fix_rotation = fix_rotation
        self.bullet = bullet

    @staticmethod
    def _calc_rect_height(r, theta):
        theta = _math.radians(theta)
        return 2 * r * _math.sin(theta / 2)

    def build_objs(self):
        super().build_objs()

        rects = []

        # Determine start & end angles.
        s = self.start_angle % 360
        e = self.end_angle % 360
        if e <= s:
            e += 360

        # Calculate resolution.
        if not self.resolution:
            self.resolution = int((e - s) / 360 * 100)

        step = (e - s) / self.resolution

        # Initialize Rectangle.
        rect_height = self._calc_rect_height(self.radius + self.thickness, step)
        rect = _o.MoveableRectangle(self.x + self.radius, self.y, 2 * self.thickness, rect_height,
                                 self.density, self.damping, fix_rotation=self.fix_rotation, bullet=self.bullet,
                                 coords_by_center=True)

        angles = [i * step + s for i in range(self.resolution)]

        # Create rectangles.
        for angle in angles:
            rects.append(_pivot(rect, angle, self.x, self.y))

        glues = []
        for i in range(len(rects) - 1):
            glues.append(_o.Glue(rects[i], rects[i + 1]))

        self._obj_cache.extend(rects)
        self._obj_cache.extend(glues)

        return self._obj_cache


class Polygon(_CustomObject, _ot.Solid, _os.Other):
    def __init__(self, *points):
        """
        Solid simple Polygon. Built using ear-clipping method.
        :param points:  Any number of (x, y) points.
        """
        super().__init__()
        self.points = points

    def build_objs(self):
        super().build_objs()

        triangles = tripy.earclip(self.points)
        for triangle in triangles:
            (x1, y1), (x2, y2), (x3, y3) = triangle
            self._obj_cache.append(_o.SolidTriangle(x1, y1, x2, y2, x3, y3))

        return self._obj_cache
