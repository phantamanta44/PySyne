"""Visualizer instances that consume frequency data to produce a visual."""
from math import sin, cos, pi
import numpy as np
from PIL import Image
from PIL.ImageDraw import Draw

from pysyne import Path


class Visualizer:
    """Abstraction representing a visualizer.."""

    def __init__(self, config, bar_window_max):
        self.config = config
        self.size = tuple(map(int, config.size.split("x")))
        self.bar_window = np.arange(0, bar_window_max, float(bar_window_max) / float(self.config.segs))

    def process(self, fft):
        raise NotImplementedError()


def vis_for(config):
    if config.circle:
        return CircleCurveVisualizer(config) if config.curve else CircleBarVisualizer(config)
    else:
        return LinearCurveVisualizer(config) if config.curve else LinearBarVisualizer(config)


class CircleCurveVisualizer(Visualizer):
    """Path visualizer for a circle."""

    def __init__(self, config):
        super().__init__(config, 0.8)
        self.path = Path()
        self.delta_angle = pi * 2 / self.config.segs

    def process(self, fft):
        fft = (fft * 10) * self.bar_window
        img = Image.new("RGB", self.size)
        offset_x, offset_y = map(lambda x: 0.5 * x, self.size)
        self.path.clear()
        for i in range(0, self.config.segs):
            pt_radius = self.config.rad + fft[i]
            self.path.point(
                pt_radius * sin(self.delta_angle * i) + offset_x,
                pt_radius * cos(self.delta_angle * i) + offset_y
            )
        self.path.curve(img)
        return img


class CircleBarVisualizer(Visualizer):
    """Bar visualizer for a circle."""

    def __init__(self, config):
        super().__init__(config, 12)

    def process(self, fft):
        raise NotImplementedError()  # TODO Implement!


class LinearCurveVisualizer(Visualizer):
    """Path visualizer in a line."""

    def __init__(self, config):
        super().__init__(config, 6)
        self.path = Path()

    def process(self, fft):
        self.path.clear()
        raise NotImplementedError()  # TODO Implement!


class LinearBarVisualizer(Visualizer):
    """Bar visualizer in a line."""

    def __init__(self, config):
        super().__init__(config, 2.4)

    def process(self, fft):
        fft = (fft * 200) * self.bar_window
        img = Image.new("RGB", self.size)
        d = Draw(img)
        bar_width = self.size[0] / self.config.segs
        half_height = self.size[1] / 2.0
        for i in range(0, self.config.segs):
            val = max(fft[i], self.config.min) / 2.0
            d.rectangle([i * bar_width, half_height - val, (i + 1) * bar_width, half_height + val])
        del d
        return img
