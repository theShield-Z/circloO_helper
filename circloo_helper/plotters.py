"""
TODO: Possibly implement other connection types
TODO: Possibly allow plotted points to be Moveable objects
TODO: Re-implement image plotter
"""

from copy import copy
from typing import Type

from .object import CustomObject
from .circloo_objects import Line, Rope, Hinge, Slider, DistanceConnection, SolidCircle


class PointPlotter(CustomObject):
    def __init__(self, obj_type: Type[Line
                                      | Rope
                                      | Slider
                                      | DistanceConnection],
                 *points,
                 close: bool = True,
                 line_thickness: int | float = 3):
        """
        Connect points in a line
        :param obj_type:    Type of circloO Object that displays a straight line.
        :param points:      Any number of (x, y) points.
        :param close:       If True, connects the ending point with the starting point to make a closed polygon;
                                default is True
        :param line_thickness:  If obj_type is Line, thickness of each line; default is 3
        """
        super().__init__()
        self.cls = obj_type
        self.points = points
        self.close = close
        self.line_thickness = line_thickness

    def build_objs(self):
        super().build_objs()

        if self.cls is Rope or self.cls is DistanceConnection:
            offset = -100_000
            l1 = Line(offset, offset, offset, offset)
            l2 = Line(offset, offset, offset, offset)
            self._obj_cache.append(l1)
            self._obj_cache.append(l2)

            for i in range(len(self.points) - 1):
                cur_x, cur_y = self.points[i]
                next_x, next_y = self.points[i + 1]

                self._obj_cache.append(self.cls(l1, l2,
                                                cur_x - offset, cur_y - offset,
                                                next_x - offset, next_y - offset))

            if self.close:
                sx, sy = self.points[0]
                ex, ey = self.points[-1]
                self._obj_cache.append(self.cls(l1, l2,
                                                ex - offset, ey - offset,
                                                sx - offset, sy - offset))

        elif self.cls is Line:
            for i in range(len(self.points) - 1):
                cur_x, cur_y = self.points[i]
                next_x, next_y = self.points[i + 1]

                self._obj_cache.append(Line(cur_x, cur_y, next_x, next_y, self.line_thickness))

            if self.close:
                sx, sy = self.points[0]
                ex, ey = self.points[-1]
                self._obj_cache.append(Line(ex, ey, sx, sy, self.line_thickness))

        elif self.cls is Slider or self.cls is Hinge:
            # ghost_rect = SolidRectangle(0, 0, 0, 0, 45, True)
            ghost_circle = SolidCircle(0, 0, -.5)

            cur_rect = copy(ghost_circle)
            next_rect = None
            sliders = []

            for i in range(len(self.points) - 1):
                cur_x, cur_y = self.points[i]
                next_x, next_y = self.points[i + 1]

                cur_rect.x = cur_x
                cur_rect.y = cur_y

                next_rect = copy(ghost_circle)
                next_rect.x = next_x
                next_rect.y = next_y

                sliders.append(self.cls(cur_rect, next_rect))
                self._obj_cache.append(cur_rect)
                cur_rect = next_rect

            if next_rect is not None:
                self._obj_cache.append(next_rect)

            if self.close:
                sliders.append(self.cls(self._obj_cache[-1], self._obj_cache[0]))

            self._obj_cache.extend(sliders)

        return self._obj_cache
