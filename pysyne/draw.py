"""Drawing utilities."""
import numpy as np
from PIL.ImageDraw import Draw


class Path:
    """Represents a list of points forming a path."""

    def __init__(self):
        self.points = []

    def clear(self):
        self.points.clear()

    def point(self, x, y):
        self.points.append((x, y))

    def curve(self, img):
        d = Draw(img)
        i, max_val = 1, len(self.points) - 2
        last_pos = self.points[0]
        while i < max_val:
            avg_pos = (
                (self.points[i][0] + self.points[i + 1][0]) / 2.0,
                (self.points[i][1] + self.points[i + 1][1]) / 2.0
            )
            _curveto(d, last_pos, self.points[i], avg_pos)
            last_pos = avg_pos
            i += 1
        _curveto(d, last_pos, self.points[i], self.points[i + 1])
        del d


def _curveto(draw, src, ctrl, dest):
    dt = 1.0 / (_dist(src, ctrl) + _dist(ctrl, dest))
    src, ctrl, dest = map(np.array, [src, ctrl, dest])
    for t in np.arange(0.0, 1.0, dt):
        p_edge = (src * t + (1 - t) * ctrl, ctrl * t + (1 - t) * dest)
        p_curve = p_edge[0] * t + (1 - t) * p_edge[1]
        draw.point((p_curve[0], p_curve[1]))


def _dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5
