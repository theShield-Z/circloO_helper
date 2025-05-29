import math as _math
import subprocess as _subprocess
from .level import Level as _Level


def polar(r, theta, start_x=1500, start_y=1500, in_degrees=True):
    """Converts a point in polar coordinates to rectangular coordinates."""
    if in_degrees:  # Angle given in degrees, convert to radians.
        theta = _math.radians(theta)

    x = r * _math.cos(theta)
    y = r * _math.sin(theta)

    # Zero precision error.
    if abs(x) < 0.000001:
        x = 0.0
    if abs(y) < 0.000001:
        y = 0.0

    # Set to center.
    x += start_x
    y += start_y

    return (x, y)


def push_to_android(file_path, destination='/sdcard'):
    """
    Pushes a file to an Android device using ADB.
    """
    try:
        command = ['adb', 'push', file_path, destination]

        result = _subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"File successfully pushed to {destination} folder.")
        else:
            print(f"Error pushing file: {result.stderr}")
    except Exception as e:
        print(f"An error has occurred: {e}")


def combine(level_1: _Level, level_2: _Level):
    new_level = level_1.copy()
    new_level.add(level_2.objs)
