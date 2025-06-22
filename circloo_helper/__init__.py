from warnings import warn

from .level import Level, parse
from .object import Object
import circloo_helper.objects
from .object_groups import ObjectGroup

import circloo_helper.mechanisms
from .tools import *
from .text import write, create_write_character
from .pixel_builder import build

try:
    from .plotters import plot_points, plot_image
    from .video_converter import video_to_circloo, BAYER_MATRIX_8X8, LINE_DITHER_8X8, DOTTED_LINE_DITHER_8X8
except ImportError:
    warn("Unable to load video converter and/or plotters. Please install opencv-python to use them.")

try:
    from .image_converter import image_to_circloo
except ImportError:
    warn("Unable to load image converter. Please install pillow to use it.")

try:
    from.svg_converter import svg_to_circloo
except ImportError:
    warn("Unable to load svg converter. Please install svgpathtools to use it.")
