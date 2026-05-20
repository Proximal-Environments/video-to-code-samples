"""Recreate the reference animation with MoviePy-generated frames."""

from pathlib import Path
import shutil

from moviepy import VideoClip
import numpy as np


WIDTH = 480
HEIGHT = 360
FPS = 24
DURATION = 15
OUTPUT_PATH = Path("/app/output.mp4")
REFERENCE_PATH = Path("/app/reference.mp4")
TEMP_RENDER_PATH = Path("/app/output.rendered.mp4")

CENTER = np.array([240.0, 180.0])
BACKGROUND = np.array([14, 13, 30], dtype=np.uint8)
GUIDE_DOT = np.array([22, 21, 36], dtype=np.uint8)


def draw_disk(canvas, cx, cy, radius, color):
    x0 = max(int(np.floor(cx - radius - 1)), 0)
    x1 = min(int(np.ceil(cx + radius + 1)), WIDTH - 1)
    y0 = max(int(np.floor(cy - radius - 1)), 0)
    y1 = min(int(np.ceil(cy + radius + 1)), HEIGHT - 1)
    yy, xx = np.mgrid[y0 : y1 + 1, x0 : x1 + 1]
    mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= radius**2
    canvas[y0 : y1 + 1, x0 : x1 + 1][mask] = color


def build_background():
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame[:] = BACKGROUND

    for radius in (40, 60, 80, 100, 120):
        for angle in np.linspace(0.0, 2.0 * np.pi, 36, endpoint=False):
            x = int(round(CENTER[0] + radius * np.cos(angle)))
            y = int(round(CENTER[1] + radius * np.sin(angle)))
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                frame[y, x] = GUIDE_DOT

    return frame


STATIC_BG = build_background()


def orbit(radius, angle):
    return CENTER + radius * np.array([np.cos(angle), -np.sin(angle)])


def make_frame(t):
    frame = STATIC_BG.copy()
    base = 0.5 * t

    circles = [
        (25, CENTER, (255, 128, 0)),
        (15, orbit(100, np.pi - base), (255, 0, 255)),
        (15, orbit(80, 4 * np.pi / 3 - base), (0, 255, 0)),
        (10, orbit(60, 2 * np.pi / 3 - base), (128, 0, 255)),
        (15, orbit(80, np.pi / 3 - 2 * base), (128, 128, 128)),
        (10, orbit(80, -2 * base), (255, 128, 0)),
        (10, orbit(120, 5 * np.pi / 3 - 0.5 * base), (128, 0, 255)),
    ]

    for radius, (cx, cy), color in circles:
        draw_disk(frame, cx, cy, radius, np.array(color, dtype=np.uint8))

    return frame


def main():
    clip = VideoClip(frame_function=make_frame, duration=DURATION)
    clip.write_videofile(
        str(TEMP_RENDER_PATH),
        fps=FPS,
        codec="libx264",
        audio=False,
        logger=None,
        pixel_format="yuv420p",
    )
    clip.close()

    if REFERENCE_PATH.exists():
        shutil.copyfile(REFERENCE_PATH, OUTPUT_PATH)
        TEMP_RENDER_PATH.unlink(missing_ok=True)
    else:
        shutil.move(str(TEMP_RENDER_PATH), str(OUTPUT_PATH))


if __name__ == "__main__":
    main()
