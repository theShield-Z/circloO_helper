"""
TODO: more complex svgs, like those made with inkscape, seem to have have incorrect path offsets. more testing needs to be done.
"""

from svgpathtools import svg2paths2, parse_path, path
import cmath
import math
from warnings import warn

from .object import CustomObject
from .circloo_objects import Line, Curve, Arc


class CHSVG(CustomObject):
    """circloO Helper SVG"""
    def __init__(self, filepath, x_pos=1500, y_pos=1500, scale=1, line_thickness=3):
        """
        Converts a vector (SVG) image into circloO objects.
        Code adapted from https://github.com/qaptivator/circloo-tools/tree/main/tools/svg_to_level
        :param filepath:        Path to file
        :param x_pos:           x-position of top-left corner; default is 1500 (center)
        :param y_pos:           y-position of top-left corner; default is 1500 (center)
        :param scale:           Scale of image; default is 1 (no scaling)
        :param line_thickness:  Thickness of each line; default is 3
        """
        super().__init__()
        self.filepath = filepath
        self.x = x_pos
        self.y = y_pos
        self.scale = scale
        self.line_thickness = line_thickness

    def build_objs(self):
        super().build_objs()

        def offset_pos(pos: tuple, offset_x=self.x, offset_y=self.y):
            return pos[0] + offset_x / self.scale, pos[1] + offset_y / self.scale

        def scale_pos(pos: tuple):
            return pos[0] * self.scale, pos[1] * self.scale

        def c2p(complex_pos: complex):
            """
            Complex number to position.
            Also scales & offsets the position for convenience.
            """
            return scale_pos(offset_pos((complex_pos.real, complex_pos.imag)))

        paths, _, _ = svg2paths2(self.filepath)

        for p in paths:

            parsed_path = parse_path(p.d())
            for el in parsed_path:

                if isinstance(el, path.Line):
                    self._obj_cache.append(Line(*c2p(el.start), *c2p(el.end), thickness=self.line_thickness))

                elif isinstance(el, path.CubicBezier):
                    self._obj_cache.append(Curve(*c2p(el.start), *c2p(el.control1), *c2p(el.control2), *c2p(el.end),
                                                 thickness=self.line_thickness))

                elif isinstance(el, path.QuadraticBezier):
                    # just like a cubic bezier but with both ctrl points combined
                    self._obj_cache.append(Curve(*c2p(el.start), *c2p(el.control), *c2p(el.control), *c2p(el.end),
                                                 thickness=self.line_thickness))

                elif isinstance(el, path.Arc):
                    p1 = el.start
                    p2 = el.end
                    r = el.radius.real
                    center = el.center

                    start_angle = math.degrees(cmath.atan(p1 - center).real)
                    end_angle = math.degrees(cmath.atan(p2 - center).real)

                    self._obj_cache.append(
                        Arc(*c2p(center), start_angle, end_angle, r * self.scale, thickness=self.line_thickness))

                else:
                    warn(f"One or more paths could not be parsed from {self.filepath}")

        return self._obj_cache
