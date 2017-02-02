"""The class that does the signal processing."""
from io import open
from math import floor
import numpy as np
from numpy.fft import fft
from subprocess import Popen, PIPE

from pysyne import vis_for


class Processor:
    """The class that does the signal processing."""

    def __init__(self, config):
        self.input = config.input
        self.output = config.output or (self.input[:(self.input.rfind(".")) or len(self.input)] + ".mp4")
        self.size = map(int, config.size.split("x"))
        self.fps = config.fps
        self.audio = config.audio
        self.segs = config.segs
        self.win = window_type(config.win)
        self.proc = None
        self.stream_out = None
        self.sample_rate = 44100
        self.vis = vis_for(config)
        self.fft_rebinned = np.zeros((self.segs,))
        self.scale_down_factor = 0.02442**(1.0 / self.fps)

    def begin(self):
        try:
            self.proc = Popen([
                "ffmpeg", "-y",
                "-f", "image2pipe",
                "-r", str(self.fps),
                "-vcodec", "mjpeg",
                "-i", "-",
                self.output
            ], stdin=PIPE)
            self.stream_out = self.proc.stdin
        except FileNotFoundError:
            raise FileNotFoundError("FFMPEG not found on the path!")

    def accept(self, roi):
        window = self.win(len(roi))
        fft_bins = np.real(fft(detrend(np.array(roi) * window)))
        rebinned = rebin(fft_bins[1:1 + int(floor(len(fft_bins) / 3.0))], self.segs)
        for i in range(0, self.segs):
            scaled_down = self.fft_rebinned[i] * self.scale_down_factor
            if rebinned[i] >= scaled_down:
                self.fft_rebinned[i] = rebinned[i]
            else:
                self.fft_rebinned[i] = scaled_down
        img = self.vis.process(self.fft_rebinned)
        img.save(self.stream_out, "JPEG")

    def finish(self):
        self.stream_out.close()
        self.proc.wait()
        if self.audio:
            Popen([
                "ffmpeg", "-y",
                "-i", self.output,
                "-i", self.input,
                "-c:v", "copy",
                "-c:a", "aac",
                self.output
            ]).wait()


def detrend(data):
    return data - np.average(data)

WINDOW_TYPES = {
    "rect": lambda bin_count: np.ones((bin_count,)),
    "bartlett": np.bartlett,
    "blackman": np.blackman,
    "hamming": np.hamming,
    "hanning": np.hanning
}


def window_type(wintype):
    return WINDOW_TYPES[wintype.lower()]


def rebin(data, bin_count):
    bins = np.empty((bin_count,))
    seg_len = int(floor(float(len(data)) / float(len(bins))))
    for i in range(0, bin_count):
        bins[i] = data[seg_len * i:seg_len * (i + 1)].mean(0)
    return bins
