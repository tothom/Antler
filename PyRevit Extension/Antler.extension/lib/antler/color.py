import math

# import clr
#
# clr.AddReference("System.Drawing")
# import System.Drawing


def hsv_to_rgb(h, s, v):
    """
    Returns color RGB values from hue, saturation and value as a tuple.

    h: Hue as float, 0 < h < 1.0
    s: Saturation as a float, 0 < s <1.0
    v: Value as a float, 0 < v <1.0

    Source:
        stackoverflow.com/questions/1335426/is-there-a-built-in-c-net-system-api-for-hsv-to-rgb

    Usage:
    hsv_to_rgb(3.14, 0.5, 1)
    """
    # h = h % (2*math.pi)

    hi = math.floor(h * 6.0) % 6
    f = h * 6.0 - math.floor(h * 6.0)

    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    switch = {
        0: (v, t, p),
        1: (q, v, p),
        2: (p, v, t),
        3: (p, q, v),
        4: (t, p, v),
    }

    return switch.get(hi, (v, p, q))


def rgb_to_hsv(r, g, b):
    """
    Source: colorsys
    """
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v





def lighten_color(color, factor=0.5):
    r, g, b = color.R, color.G, color.B
    # return System.Drawing.Color.FromArgb(r, g, b)


def random_color(seed):
    pass
