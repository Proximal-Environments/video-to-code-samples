"""Four shapes that morph: circle -> square -> 4-lobe flower.

The 20s animation has four 5s phases:
  [ 0- 5s] hold circle
  [ 5-10s] morph to square (superellipse exponent grows: |x|^n + |y|^n = R^n)
  [10-15s] hold square
  [15-20s] morph to 4-lobe (each side bows outward into a circular arc that
           passes through the corners (R, +/-R) with apex at (R+e, 0))
"""
from moviepy import VideoClip
import numpy as np

W, H = 480, 360
FPS = 24
DURATION = 20.0
R = 25.5

# BG is shifted slightly so libx264's YUV roundtrip lands on (19, 9, 29).
BG = np.array([20, 10, 30], dtype=np.float32)
ORANGE = np.array([254, 127, 0], dtype=np.float32)
GRAY = np.array([128, 128, 128], dtype=np.float32)
BLUE = np.array([0, 0, 254], dtype=np.float32)

SHAPES = [
    (64.6, 179.5, ORANGE),
    (180.6, 179.5, GRAY),
    (297.5, 179.5, ORANGE),
    (414.6, 179.5, BLUE),
]

# Bulge depth at phase-4 end: arc through (R,0),(R,R) with apex (R+E_MAX, R/2)
# matches the 4-circle union (centers at (+/-R/2,+/-R/2), radius R/sqrt(2)).
E_MAX = R * (1.0 / np.sqrt(2) - 0.5)

ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)


def inside_shape(t, abs_x, abs_y):
    """Boolean mask of pixels inside the morphing shape at time t."""
    if t <= 5.0:
        return abs_x * abs_x + abs_y * abs_y <= R * R
    if t <= 10.0:
        # 1/n linear from 0.5 (circle) to ~0 (square)
        inv_n = 0.5 * (1.0 - (t - 5.0) / 5.0)
        if inv_n < 1e-3:
            return (abs_x <= R) & (abs_y <= R)
        n = 1.0 / inv_n
        return (abs_x / R) ** n + (abs_y / R) ** n <= 1.0
    if t <= 15.0:
        return (abs_x <= R) & (abs_y <= R)
    # Phase 4: arc bows outward; 4-fold symmetric, so test against |u| <= arc(|v|).
    alpha = min(1.0, (t - 15.0) / 5.0)
    e = E_MAX * alpha
    if e < 1e-3:
        return (abs_x <= R) & (abs_y <= R)
    h = R + 0.5 * e - R * R / (8.0 * e)
    rho = R + e - h
    u = np.maximum(abs_x, abs_y)
    v = np.minimum(abs_x, abs_y)
    v_clamped = np.minimum(v, R)
    arc_x = h + np.sqrt(np.maximum(0.0, rho * rho - (v_clamped - 0.5 * R) ** 2))
    return (v <= R) & (u <= arc_x)


def make_frame(t):
    frame = np.broadcast_to(BG, (H, W, 3)).copy()
    for cx, cy, color in SHAPES:
        mask = inside_shape(t, np.abs(xs - cx), np.abs(ys - cy))
        frame[mask] = color
    return np.clip(frame, 0, 255).astype(np.uint8)


def main():
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        "/app/output.mp4",
        fps=FPS,
        logger=None,
        codec="libx264",
        ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "10"],
    )


if __name__ == "__main__":
    main()
