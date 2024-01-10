from PyQt6.QtGui import QColor


def linearInterpolate(val1, val2, t):
    return val1 * (1.0 - t) + val2 * t


def linearInterpolateColor(color1: QColor, color2: QColor, t: float):
    red = linearInterpolate(color1.red(), color2.red(), t)
    green = linearInterpolate(color1.green(), color2.green(), t)
    blue = linearInterpolate(color1.blue(), color2.blue(), t)

    return QColor(int(red), int(green), int(blue))
