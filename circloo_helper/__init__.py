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

import circloo_helper.dithering
from .image_converter import CHImage
from .video_converter import CHVideo

from .plotters import PointPlotter

# try:
#     from.svg_converter import svg_to_circloo
# except ImportError:
#     warn("Unable to load svg converter. Please install svgpathtools to use it.")
