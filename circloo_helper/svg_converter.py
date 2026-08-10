"""
TODO: implement filled paths using the Polygon custom object or hatching
TODO: also convert embedded images using CHImage
TODO: Replace svgpathtools with a more reliable library
"""

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

    def _build_objs(self):
        super()._build_objs()

        try:
            from svgpathtools import svg2paths2, parse_path, path, Document
        except ImportError as e:
            raise ImportError("Install 'svg' extras: svgpathtools-light") from e

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

        def is_elliptical_arc(seg, rel_tol=1e-9):
            if not isinstance(seg, path.Arc):
                return False

            rx = seg.radius.real
            ry = seg.radius.imag

            return not math.isclose(rx, ry, rel_tol=rel_tol)

        doc = Document(self.filepath)
        paths = doc.paths()

        for p_ in paths:
            # Convert elliptical Arcs into curves (circloO Arcs must be circular)
            p = path.Path()
            for el in parse_path(p_.d()):
                if isinstance(el, path.Arc) and is_elliptical_arc(el):
                    p.extend(el.as_cubic_curves(curves=2))
                else:
                    p.append(el)

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
                    warn(f"One or more paths could not be parsed from {self.filepath}: {p}")

        return self._obj_cache
