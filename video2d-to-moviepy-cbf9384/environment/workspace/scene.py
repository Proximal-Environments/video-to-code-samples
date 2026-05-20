"""Build your animation using MoviePy."""
from moviepy import *
import numpy as np


def main():
    # TODO: study reference.mp4 and recreate the animation here
    clip = ColorClip(size=(480, 360), color=(0, 0, 0), duration=3)
    clip.write_videofile("/app/output.mp4", fps=24, logger=None)


if __name__ == "__main__":
    main()
