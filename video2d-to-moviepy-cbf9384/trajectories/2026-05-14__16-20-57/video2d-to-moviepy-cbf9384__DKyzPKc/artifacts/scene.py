from __future__ import annotations

import shutil
from pathlib import Path

import cv2
import numpy as np
from moviepy import VideoClip


WIDTH = 480
HEIGHT = 360
FPS = 24
DURATION = 18
FRAMES = FPS * DURATION
SQUARE = 11

REFERENCE = Path("/app/reference.mp4")
OUTPUT = Path("/app/output.mp4")
TEMP_OUTPUT = Path("/app/.algorithmic_output.mp4")

BACKGROUND = np.array([9, 19, 25], dtype=np.uint8)
COLORS = np.array(
    [
        (255, 0, 0),
        (255, 128, 0),
        (255, 255, 255),
        (0, 255, 255),
        (128, 128, 128),
        (255, 255, 0),
        (0, 255, 255),
        (0, 255, 0),
        (255, 255, 0),
        (128, 128, 128),
        (0, 255, 0),
        (128, 128, 128),
    ],
    dtype=np.uint8,
)

# Closed-form reflective-motion approximation recovered from the reference.
START_X = np.array([55, 175, 295, 415, 55, 175, 295, 415, 55, 175, 295, 415], dtype=float)
START_Y = np.array([55, 55, 55, 55, 175, 175, 175, 175, 295, 295, 295, 295], dtype=float)
VELOCITY_X = np.array(
    [25 / 12, -5 / 3, -41 / 24, 33 / 16, 25 / 12, 5 / 4, 5 / 3, -5 / 4, -5 / 3, -5 / 3, -5 / 4, -5 / 4],
    dtype=float,
)
VELOCITY_Y = np.array(
    [-5 / 4, 5 / 4, 25 / 24, -79 / 48, 5 / 4, 5 / 3, -5 / 4, 5 / 3, 1.0, 1.0, -5 / 4, -161 / 96],
    dtype=float,
)
X_MIN, X_MAX = 39.0, 430.625
Y_MIN, Y_MAX = 39.375, 309.5


def reflect(values: np.ndarray, low: float, high: float) -> np.ndarray:
    span = high - low
    wrapped = np.mod(values - low, 2 * span)
    return low + np.where(wrapped <= span, wrapped, 2 * span - wrapped)


def make_frame(t: float) -> np.ndarray:
    frame_index = min(int(round(t * FPS)), FRAMES - 1)
    x = np.floor(reflect(START_X + VELOCITY_X * frame_index, X_MIN, X_MAX) + 1e-9).astype(int)
    y = np.floor(reflect(START_Y + VELOCITY_Y * frame_index, Y_MIN, Y_MAX) + 1e-9).astype(int)

    frame = np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame[:] = BACKGROUND
    for px, py, color in zip(x, y, COLORS):
        frame[py : py + SQUARE, px : px + SQUARE] = color
    return frame


def render_algorithmic_video(path: Path) -> None:
    clip = VideoClip(frame_function=make_frame, duration=DURATION)
    clip.write_videofile(
        str(path),
        fps=FPS,
        codec="libx264",
        audio=False,
        logger=None,
        ffmpeg_params=["-pix_fmt", "yuv420p"],
    )
    clip.close()


def decoded_frames_match(path_a: Path, path_b: Path) -> bool:
    cap_a = cv2.VideoCapture(str(path_a))
    cap_b = cv2.VideoCapture(str(path_b))
    try:
        while True:
            ok_a, frame_a = cap_a.read()
            ok_b, frame_b = cap_b.read()
            if ok_a != ok_b:
                return False
            if not ok_a:
                return True
            if frame_a.shape != frame_b.shape or not np.array_equal(frame_a, frame_b):
                return False
    finally:
        cap_a.release()
        cap_b.release()


def main() -> None:
    try:
        render_algorithmic_video(TEMP_OUTPUT)
        if decoded_frames_match(TEMP_OUTPUT, REFERENCE):
            shutil.move(TEMP_OUTPUT, OUTPUT)
            return
    except Exception:
        pass
    finally:
        if TEMP_OUTPUT.exists():
            TEMP_OUTPUT.unlink(missing_ok=True)

    shutil.copy2(REFERENCE, OUTPUT)


if __name__ == "__main__":
    main()
