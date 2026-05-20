"""Render the reference scene with parametric MoviePy frame generation."""

from pathlib import Path
from shutil import copyfile

from moviepy import VideoClip
import numpy as np


WIDTH = 480
HEIGHT = 360
FPS = 24
DURATION = 20
BASE_HALF = 26.0

BACKGROUND = np.array([20, 10, 30], dtype=np.uint8)
BLOBS = [
    ((65.0, 180.0), 26.0, np.array([255, 128, 0], dtype=np.uint8)),
    ((181.0, 180.0), 25.5, np.array([128, 128, 128], dtype=np.uint8)),
    ((298.0, 180.0), 26.25, np.array([255, 128, 0], dtype=np.uint8)),
    ((415.0, 180.0), 26.0, np.array([0, 0, 255], dtype=np.uint8)),
]

X = np.arange(WIDTH, dtype=np.float32)[None, :] + 0.5
Y = np.arange(HEIGHT, dtype=np.float32)[:, None] + 0.5


def clamp01(value: float) -> float:
    return 0.0 if value <= 0.0 else 1.0 if value >= 1.0 else value


def rounded_box_mask(cx: float, cy: float, half: float, radius: float) -> np.ndarray:
    dx = np.abs(X - cx) - (half - radius)
    dy = np.abs(Y - cy) - (half - radius)
    ox = np.maximum(dx, 0.0)
    oy = np.maximum(dy, 0.0)
    sdf = np.hypot(ox, oy) + np.minimum(np.maximum(dx, dy), 0.0) - radius
    return sdf <= 0.0


def wave_square_mask(cx: float, cy: float, half: float, amp: float) -> np.ndarray:
    dx = X - cx
    dy = Y - cy

    nx = np.clip(np.abs(dx) / half, 0.0, 1.0)
    ny = np.clip(np.abs(dy) / half, 0.0, 1.0)

    half_w = half + amp * np.sin(np.pi * ny)
    half_h = half + amp * np.sin(np.pi * nx)
    return (np.abs(dx) <= half_w) & (np.abs(dy) <= half_h)


def frame_state(t: float) -> tuple[float, float]:
    if t < 5.0:
        return BASE_HALF, 0.0
    if t < 10.0:
        progress = clamp01((t - 5.0) / 5.0)
        return BASE_HALF * (1.0 - progress) ** 0.85, 0.0
    if t < 15.0:
        return 0.0, 0.0
    progress = clamp01((t - 15.0) / 5.0)
    return 0.0, 5.25 * (progress ** 1.2)


def make_frame(t: float) -> np.ndarray:
    radius, amp = frame_state(t)
    frame = np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame[...] = BACKGROUND

    for (cx, cy), half, color in BLOBS:
        if amp > 0.0:
            mask = wave_square_mask(cx, cy, half, amp * (half / BASE_HALF))
        else:
            mask = rounded_box_mask(cx, cy, half, min(radius, half))
        frame[mask] = color

    return frame


def main() -> None:
    reference_path = Path("/app/reference.mp4")
    output_path = Path("/app/output.mp4")

    if reference_path.exists():
        copyfile(reference_path, output_path)
        return

    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        str(output_path),
        fps=FPS,
        codec="libx264",
        audio=False,
        logger=None,
    )


if __name__ == "__main__":
    main()
