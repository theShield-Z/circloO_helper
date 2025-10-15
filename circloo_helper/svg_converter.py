from svgpathtools import (svg2paths2 as _svg2paths2,
                          parse_path as _parse_path,
                          path as _path)
import cmath
import math
import circloo_helper as ch


def svg_to_circloo(svg_path, x_pos=1500, y_pos=1500, scale=1, line_thickness=3):
    """
    Converts a vector image into circloO objects.
    Code adapted from https://github.com/qaptivator/circloo-tools/tree/main/tools/svg_to_level
    :param svg_path:        Path to file.
    :param x_pos:           X position of top-left corner; default is 1500 (center)
    :param y_pos:           Y position of top-left corner; default is 1500 (center)
    :param scale:           Scale of image; default is 1
    :param line_thickness:  Thickness of each line; default is 3
    :return:        List of circloO objects.
    """
    def offset_pos(pos: tuple, offset_x=x_pos, offset_y=y_pos):
        return pos[0] + offset_x/scale, pos[1] + offset_y/scale

    def scale_pos(pos: tuple):
        return pos[0] * scale, pos[1] * scale

    def c2p(complex_pos: complex):
        """Complex number to position"""
        return scale_pos(offset_pos((complex_pos.real, complex_pos.imag)))

    paths, _, _ = _svg2paths2(svg_path)
    objs = []

    for path in paths:

        parsed_path = _parse_path(path.d())
        for el in parsed_path:
            # Loop through each element of the path.

            if isinstance(el, _path.Line):
                objs.append(ch.objects.Line(*c2p(el.start), *c2p(el.end), thickness=line_thickness))

            elif isinstance(el, _path.CubicBezier):
                objs.append(ch.objects.Curve(*c2p(el.start), *c2p(el.control1), *c2p(el.control2), *c2p(el.end),
                                             thickness=line_thickness))

            elif isinstance(el, _path.QuadraticBezier):
                # just like a cubic bezier but with both ctrl points combined
                objs.append(ch.objects.Curve(*c2p(el.start), *c2p(el.control), *c2p(el.control), *c2p(el.end),
                                             thickness=line_thickness))

            elif isinstance(el, _path.Arc):
                p1 = el.start
                p2 = el.end
                r = el.radius.real
                center = el.center

                start_angle = math.degrees(cmath.atan(p1-center).real)
                end_angle = math.degrees(cmath.atan(p2-center).real)

                objs.append(ch.objects.Arc(*c2p(center), start_angle, end_angle, r * scale, thickness=line_thickness))

    return objs
