import math as _math


def polar(r, theta, degrees=True):
    """Converts a point in polar coordinates to rectangular coordinates"""
    if degrees:  # Angle given in degrees, convert to radians.
        theta = _math.radians(theta)

    x = r * _math.cos(theta)
    y = r * _math.sin(theta)

    # Zero precision error.
    if abs(x) < 0.000001:
        x = 0.0
    if abs(y) < 0.000001:
        y = 0.0

    # Set to center.
    x += 1500
    y += 1500

    return (x, y)
