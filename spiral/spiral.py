"""This module creates an Archimdean Spiral."""

from math import cos, sin, pi
import win32api
import time
widht = 1366
hight = 768

theta = 0.0
step = 0.5
loops = 5
a = 5
b = 5
while theta < 2 * loops * pi:
    theta += step
    r = a + b * theta
    x = int(widht / 2 + (r * cos(theta)) * 2)
    y = int(hight / 2 + (r * sin(theta)))
    time.sleep(0.1)
    win32api.SetCursorPos((x, y))
