import math as _math
import tripy as _tripy

from .object import CustomObject as _CustomObject
import circloo_helper.circloo_objects as _o
import circloo_helper.object_types as _types
import circloo_helper.object_shapes as _shapes
from .tools import (
    pivot as _pivot,
    polar as _polar
)


class OutlineRectangle(_CustomObject, _types.Solid, _shapes.Rectangle, _shapes.Line):
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

    def _build_objs(self):
        super()._build_objs()
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


class MoveableArc(_CustomObject, _types.Moveable, _shapes.Line):
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
        :param end_angle:       Ending angle in degrees; default is 360 (full circle)
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

    def _build_objs(self):
        super()._build_objs()

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
                                 self.density, self.damping, bullet=self.bullet,
                                 coords_by_center=True)

        angles = [i * step + s for i in range(self.resolution)]

        # Create rectangles.
        for angle in angles:
            rects.append(_pivot(rect, angle, self.x, self.y))

        if self.fix_rotation:   # Avoids putting the modifier on every rect, reducing file size
            rects[0].fix_rotation = True

        glues = []
        for i in range(len(rects) - 1):
            glues.append(_o.Glue(rects[i], rects[i + 1]))

        self._obj_cache.extend(rects)
        self._obj_cache.extend(glues)

        return self._obj_cache


class Polygon(_CustomObject, _types.Solid, _shapes.Other):
    def __init__(self, *points):
        """
        Solid simple Polygon. Built using ear-clipping method.
        :param points:  Any number of (x, y) points.
        """
        super().__init__()
        self.points = points

    def _build_objs(self):
        super()._build_objs()

        triangles = _tripy.earclip(self.points)
        for triangle in triangles:
            (x1, y1), (x2, y2), (x3, y3) = triangle
            self._obj_cache.append(_o.SolidTriangle(x1, y1, x2, y2, x3, y3))

        return self._obj_cache


class Star(_CustomObject, _types.Solid, _shapes.Other):
    def __init__(self,
                 x_pos,
                 y_pos,
                 outer_radius: int | float,
                 inner_radius: int | float | None = None,
                 n_points: int = 5,
                 rotation: int | float = -90):
        """
        Solid n-pointed star.
        :param x_pos:           X-position of center of Star
        :param y_pos:           Y-position of center of Star
        :param outer_radius:    Radius of outer set of points of Star
        :param inner_radius:    Radius of inner set of points of Star; if None, this radius will be set
                                    automatically to form a regular star; default is None
        :param n_points:        Number of points on the Star; default is 5
        :param rotation:        Rotation in degrees of Star; 0 points the star to the right; default is -90 (upright)
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.outer_radius = outer_radius
        self.rotation = rotation

        if n_points > 0:
            self.n_points = n_points
        else:
            raise ValueError("n_points of a Star must be positive and nonzero.")

        if inner_radius is None:
            pi = _math.pi
            cos = _math.cos
            n = self.n_points
            self.inner_radius = outer_radius * cos(2 * pi / n) / cos(pi / n)
        else:
            self.inner_radius = inner_radius

    def _build_objs(self):
        super()._build_objs()

        points = []

        step = 360 / (self.n_points * 2)
        angles = []
        t = 0
        while t < 360:
            angles.append(t + self.rotation)
            t += step

        for i, angle in enumerate(angles):
            if i % 2 == 0:
                # outer point
                points.append(_polar(self.outer_radius, angle, self.x, self.y))
            else:
                # inner point
                points.append(_polar(self.inner_radius, angle, self.x, self.y))

        self._obj_cache.extend(Polygon(*points).get_objs())

        return self._obj_cache


class PauseDetector(_CustomObject, _shapes.Other):
    def __init__(self, x: int | float, y: int | float):
        """
        Detects when the Pause button has been pressed.
        The output_trigger attribute is only available after PauseDetector.get_objects() has been called.

        This mechanism is very sensitive to object order--editing a level with this a PauseDetector in-game may cause it
        to break. It is recommended to add this to a level only after all in-game editing is finished.

        :param x: X-position of mechanism's center.
        :param y: Y-position of mechanism's center.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.output_trigger: None | _o.SpecialCollectable = None

    def _build_objs(self):
        super()._build_objs()
        self.output_trigger = _o.SpecialCollectable(self.x - 50, self.y - 25, is_trigger=True, collect_from_object=True)

        # Physical Objects.

        out_gen = _o.CircleGenerator(self.x - 50, self.y - 25, 15, 0.01, 0, 9999, start_off=True, no_fade=True)
        anchor = _o.SolidCircle(self.x + 50, self.y - 25, 15)

        anchor_trig_1 = _o.SpecialCollectable(self.x + 50, self.y - 25, is_trigger=True, collect_from_object=True)
        anchor_trig_1.mute()
        anchor_trig_2 = _o.SpecialCollectable(self.x + 50, self.y - 25, is_trigger=True, collect_from_object=True)
        anchor_trig_2.mute()
        anchor_trig_3 = _o.SpecialCollectable(self.x + 50, self.y - 25, is_trigger=True, collect_from_object=True)
        anchor_trig_3.mute()

        loop_gen_1 = _o.CircleGenerator(self.x - 50, self.y + 25, 15, 0, 0, 9999, no_fade=True)
        loop_gen_2 = _o.CircleGenerator(self.x, self.y + 25, 15, 0, 0, 9999, no_fade=True, start_off=True)
        loop_gen_3 = _o.CircleGenerator(self.x + 50, self.y + 25, 15, 0, 0, 9999, no_fade=True, start_off=True)

        loop_trig_1 = _o.SpecialCollectable(self.x - 50, self.y + 25, is_trigger=True, collect_from_object=True)
        loop_trig_1.mute()
        loop_trig_2 = _o.SpecialCollectable(self.x, self.y + 25, is_trigger=True, collect_from_object=True)
        loop_trig_2.mute()
        loop_trig_3 = _o.SpecialCollectable(self.x + 50, self.y + 25, is_trigger=True, collect_from_object=True)
        loop_trig_3.mute()

        # Instantly pulls output generator to the anchor, unless game is paused.
        rope = _o.Rope(out_gen, anchor, max_length=-100)

        # Special Connections.

        # Spawn/Destroy output generator.
        out_spawn_1 = _o.SpecialConnection(loop_trig_1, out_gen, 'NowIf')
        out_spawn_2 = _o.SpecialConnection(loop_trig_2, out_gen, 'NowIf')
        out_spawn_3 = _o.SpecialConnection(loop_trig_3, out_gen, 'NowIf')
        out_destroy_1 = _o.SpecialConnection(anchor_trig_1, out_gen, 'Destroy')
        out_destroy_2 = _o.SpecialConnection(anchor_trig_2, out_gen, 'Destroy')
        out_destroy_3 = _o.SpecialConnection(anchor_trig_3, out_gen, 'Destroy')

        # Loop connections.
        l1_dest = _o.SpecialConnection(loop_trig_1, loop_gen_1, 'Destroy')
        l1_spawn_l2 = _o.SpecialConnection(loop_trig_1, loop_gen_2, 'NowIf')
        l2_dest = _o.SpecialConnection(loop_trig_2, loop_gen_2, 'Destroy')
        l2_spawn_l3 = _o.SpecialConnection(loop_trig_2, loop_gen_3, 'NowIf')
        l3_dest = _o.SpecialConnection(loop_trig_3, loop_gen_3, 'Destroy')
        l3_spawn_l1 = _o.SpecialConnection(loop_trig_3, loop_gen_1, 'NowIf')

        # Anchor trigger loop connections.
        anchor_reactivate_12 = _o.SpecialConnection(anchor_trig_1, anchor_trig_2, 'Reactivate')
        anchor_reactivate_23 = _o.SpecialConnection(anchor_trig_2, anchor_trig_3, 'Reactivate')
        anchor_reactivate_31 = _o.SpecialConnection(anchor_trig_3, anchor_trig_1, 'Reactivate')
        anchor_deactivate_13 = _o.SpecialConnection(anchor_trig_1, anchor_trig_3, 'Deactivate')
        anchor_deactivate_32 = _o.SpecialConnection(anchor_trig_3, anchor_trig_2, 'Deactivate')
        anchor_deactivate_21 = _o.SpecialConnection(anchor_trig_2, anchor_trig_1, 'Deactivate')

        # All objects must be added in a very specific order to work.
        self._obj_cache.extend([
            out_gen, anchor_trig_1, anchor_trig_2, loop_trig_1, loop_trig_2, loop_trig_3,
            loop_gen_3, loop_gen_2, loop_gen_1, anchor, anchor_trig_3, self.output_trigger,
            rope, l1_dest, anchor_reactivate_23, out_spawn_3, anchor_reactivate_31, l3_spawn_l1,
            anchor_reactivate_12, l2_dest, l3_dest, l1_spawn_l2, l2_spawn_l3, out_destroy_3,
            out_spawn_1, out_spawn_2, out_destroy_2, out_destroy_1, anchor_deactivate_13, anchor_deactivate_32,
            anchor_deactivate_21
        ])

        return self._obj_cache
