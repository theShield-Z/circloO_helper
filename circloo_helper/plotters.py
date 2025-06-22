import cv2 as _cv
import numpy as _np
import circloo_helper.objects as _objects
from .level import Level as _Level


def get_all_edge_points(image_path, resolution=100):
    # Load image in grayscale
    img = _cv.imread(image_path, _cv.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Threshold the image to binary (invert if shapes are black on white)
    _, thresh = _cv.threshold(img, 127, 255, _cv.THRESH_BINARY_INV)

    # Find all external contours
    contours, _ = _cv.findContours(thresh, _cv.RETR_EXTERNAL, _cv.CHAIN_APPROX_NONE)
    if not contours:
        raise ValueError("No contours found in the image.")

    # Sort contours by area (optional)
    # contours = sorted(contours, key=_cv.contourArea, reverse=True)

    # Distribute resolution equally across all contours
    num_shapes = len(contours)
    points_per_shape = max(1, resolution // num_shapes)
    all_sampled_points = []

    for contour in contours:
        contour = contour[:, 0, :]  # Flatten shape to (N, 2)
        if len(contour) == 0:
            continue

        # Sample points evenly along contour
        indices = _np.linspace(0, len(contour) - 1, points_per_shape, dtype=int)
        sampled = contour[indices]
        all_sampled_points.append([tuple(pt) for pt in sampled])

    return all_sampled_points


def line_plotter(points: list[tuple], thickness=3, close=False):
    lines = []
    for i in range(len(points) - 1):
        lines.append(_objects.Line(*points[i], *points[i+1], thickness=thickness))
    if close:
        lines.append(_objects.Line(*points[-1], *points[-0], thickness=thickness))
    return lines


def rope_plotter(points: list[tuple], close=False):
    objs = []
    line_1 = _objects.Line(0, 0, 0, 0)
    line_2 = _objects.Line(0, 0, 0, 0)
    objs.append([line_1, line_2])
    for i in range(len(points)-1):
        objs.append(_objects.Rope(line_1, line_2, *points[i], *points[i+1]))
    if close:
        objs.append(_objects.Rope(line_1, line_2, *points[-1], *points[0]))
    return objs


def plot_points(points: list[tuple], mode, close=False, line_thickness=3):
    """
    Given a list of points as tuples, connects the points with the object chosen by mode.
    :param points:          List of points as tuples
    :param mode:            Chooses which object to plot the image out of; currently only "rope" or "line"
    :param close:           If True, connects the ending point with the starting point; default is False
    :param line_thickness:  If plotting with lines, thickness of each line; defualt is 3
    :return:
    """
    match mode:
        case "line":
            return line_plotter(points, line_thickness, close)

        case "rope":
            return rope_plotter(points, close)


def adjust_points(points: list[tuple], start_x, start_y, scale):
    """Adjust the starting position and scale of a list of points for image plotter."""
    for i in range(len(points)):
        points[i] = (scale * points[i][0] + start_x, scale * points[i][1] + start_y)


def plot_image(image_path: str, x: int | float = 1500, y: int | float = 1500, scale: int | float = 1,
               mode: str = "rope", resolution: int = 1000, line_thickness: int | float = 3):
    """
    Plot an image.
    :param image_path:      Path to image.
    :param x:               X position of top-left corner; default is 1500 (center)
    :param y:               Y position of top-left corner; default is 1500 (center)
    :param mode:            Chooses which object to plot the image out of; currently only "rope" or "line"
    :param resolution:      Number of objects to plot the image out of; defualt is 1000
    :param line_thickness:  If plotting with lines, thickness of each line; default is 3
    :return:            List of circloO objects
    """

    points = get_all_edge_points(image_path, resolution)
    objs = []

    for shape in points:
        adjust_points(shape, x, y, scale)
        objs.append(plot_points(shape, mode, True, line_thickness))

    return objs
