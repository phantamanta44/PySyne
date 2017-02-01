"""The application's entry point."""
import argparse
from math import floor
import soundfile as sf

from pysyne import Processor, WINDOW_TYPES

parser = argparse.ArgumentParser(prog="pysyne", description="Creates a visualization for an audio file.")
parser.add_argument("-o", "--output", type=str, default=None, dest="output")
parser.add_argument("-s", "--size", type=str, default="1280x720", dest="size")
parser.add_argument("-f", "--framerate", type=int, default=30, dest="fps")
parser.add_argument("-n", "--segments", type=int, default=80, dest="segs")
parser.add_argument("-m", "--min", type=float, default=2, dest="min")
parser.add_argument("-c", "--colour", type=int, default=0xFFFFFF, dest="col")
parser.add_argument("-R", "--rainbow", action="store_true", default=False, dest="rbw")
parser.add_argument("-e", "--circle", action="store_true", default=False, dest="circle")
parser.add_argument("-r", "--radius", type=float, default=100, dest="rad")
parser.add_argument("-C", "--curve", action="store_true", default=False, dest="curve")
parser.add_argument("-t", "--thickness", type=int, default=2, dest="lthk")
parser.add_argument("-w", "--window", type=str, default="hanning", choices=WINDOW_TYPES.keys(), dest="win")
parser.add_argument("input", type=str)


def main():
    config = parser.parse_args()

    snd, rate = sf.read(config.input)
    snd = snd[:, 0]
    ttl_samples = len(snd)
    delta_sample = int(floor(float(rate) / float(config.fps)))

    proc = Processor(config)
    proc.sample_rate = rate

    proc.begin()
    for i in range(0, len(snd), delta_sample):
        if i + 1024 < ttl_samples:
            proc.accept(snd[i:i + 1024])
    proc.finish()

if __name__ == "__main__":
    main()
