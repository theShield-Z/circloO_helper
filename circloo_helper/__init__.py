from warnings import warn as _warn

from .level import Level
from .level_parser import parse, read_file, read_clipboard

import circloo_helper.object_shapes
import circloo_helper.object_types

from .object import Object, CustomObject
import circloo_helper.circloo_objects
import circloo_helper.custom_objects

from .tools import *
from .pixel_builder import Pixels
from .text import Text

from .image_converter import CHImage
from .video_converter import CHVideo

# try:
#     from .plotters import plot_points, plot_image
#     from .video_converter import video_to_circloo, BAYER_MATRIX_8X8, LINE_DITHER_8X8, DOTTED_LINE_DITHER_8X8
# except ImportError:
#     warn("Unable to load video converter and/or plotters. Please install opencv-python to use them.")
#
# try:
#     from.svg_converter import svg_to_circloo
# except ImportError:
#     warn("Unable to load svg converter. Please install svgpathtools to use it.")
