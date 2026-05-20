"""Recreate animation: 12 colored squares bouncing in canvas."""
from moviepy import VideoClip
import numpy as np

W, H = 480, 360
FPS = 24
DURATION = 18.0
SQ = 10
BG = np.array([9, 19, 25], dtype=np.uint8)

# (initial top-left x, y, color, vx, vy) — top-left positions and per-frame velocities
SQUARES = [
    ( 56,  56, (255,   0,   0),  2.083, -1.333),  # red
    (176,  56, (255, 128,   0), -1.667,  1.333),  # orange
    (296,  56, (255, 255, 255), -1.833,  1.000),  # white
    (416,  56, (  0, 255, 255),  2.000, -1.667),  # cyan
    ( 56, 176, (128, 128, 128),  2.000,  1.167),  # gray
    (176, 176, (255, 255,   0),  1.167,  1.500),  # yellow
    (296, 176, (  0, 255, 255),  1.667, -1.333),  # cyan
    (416, 176, (  0, 255,   0), -1.333,  1.667),  # green
    ( 56, 296, (255, 255,   0), -1.667,  1.000),  # yellow
    (176, 296, (128, 128, 128), -1.667,  1.000),  # gray
    (296, 296, (  0, 255,   0), -1.333, -1.333),  # green
    (416, 296, (128, 128, 128), -1.333, -1.833),  # gray
]

# Bouncing box: top-left can range over [0, W-SQ] x [0, H-SQ]
MAX_X = W - SQ
MAX_Y = H - SQ


def reflect(p, max_p):
    """Reflect coordinate p in [0, max_p] (elastic bouncing)."""
    period = 2 * max_p
    p = ((p % period) + period) % period
    if p > max_p:
        p = period - p
    return p


def render_frame(t):
    frame = np.empty((H, W, 3), dtype=np.uint8)
    frame[:] = BG
    f = t * FPS
    for x0, y0, color, vx, vy in SQUARES:
        x = reflect(x0 + vx * f, MAX_X)
        y = reflect(y0 + vy * f, MAX_Y)
        xi, yi = int(round(x)), int(round(y))
        frame[yi:yi+SQ, xi:xi+SQ] = color
    return frame


def main():
    clip = VideoClip(render_frame, duration=DURATION)
    clip.write_videofile("/app/output.mp4", fps=FPS, codec="libx264", logger=None)


if __name__ == "__main__":
    main()
