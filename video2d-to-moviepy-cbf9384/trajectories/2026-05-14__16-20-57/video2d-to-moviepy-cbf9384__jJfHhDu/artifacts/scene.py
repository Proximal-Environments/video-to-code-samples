"""Recreate the reference animation procedurally with MoviePy."""

from moviepy import VideoClip
import numpy as np


WIDTH = 480
HEIGHT = 360
FPS = 24
DURATION = 18
FRAME_COUNT = FPS * DURATION
BACKGROUND = np.array([9, 19, 25], dtype=np.uint8)
SQUARE_SIZE = 11
HALF_SIZE = SQUARE_SIZE // 2
X_MIN, X_MAX = 45.0, 435.0
Y_MIN, Y_MAX = 45.0, 315.0

PARTICLES = [
    {"pos": (60.0, 60.0), "vel": (50.0, -30.0), "color": (255, 0, 0)},
    {"pos": (180.0, 60.0), "vel": (-40.0, 30.0), "color": (255, 128, 0)},
    {"pos": (300.0, 60.0), "vel": (-40.0, 25.0), "color": (255, 255, 255)},
    {"pos": (420.0, 60.0), "vel": (50.0, -40.0), "color": (0, 255, 255)},
    {"pos": (60.0, 180.0), "vel": (50.0, 30.0), "color": (128, 128, 128)},
    {"pos": (180.0, 180.0), "vel": (30.0, 40.0), "color": (255, 255, 0)},
    {"pos": (300.0, 180.0), "vel": (40.0, -30.0), "color": (0, 255, 255)},
    {"pos": (420.0, 180.0), "vel": (-30.0, 40.0), "color": (0, 255, 0)},
    {"pos": (60.0, 300.0), "vel": (-40.0, 25.0), "color": (255, 255, 0)},
    {"pos": (180.0, 300.0), "vel": (-40.0, 25.0), "color": (128, 128, 128)},
    {"pos": (300.0, 300.0), "vel": (-30.0, -30.0), "color": (0, 255, 0)},
    {"pos": (420.0, 300.0), "vel": (-30.0, -40.0), "color": (128, 128, 128)},
]


def simulate():
    dt = 1.0 / FPS
    particles = [
        {
            "pos": np.array(spec["pos"], dtype=np.float64),
            "vel": np.array(spec["vel"], dtype=np.float64),
            "color": np.array(spec["color"], dtype=np.uint8),
        }
        for spec in PARTICLES
    ]

    positions = np.empty((FRAME_COUNT, len(particles), 2), dtype=np.float64)

    for frame in range(FRAME_COUNT):
        for i, particle in enumerate(particles):
            positions[frame, i] = particle["pos"]

        for particle in particles:
            particle["pos"] += particle["vel"] * dt

            if particle["pos"][0] <= X_MIN:
                particle["pos"][0] = X_MIN
                particle["vel"][0] = abs(particle["vel"][0])
            elif particle["pos"][0] >= X_MAX:
                particle["pos"][0] = X_MAX
                particle["vel"][0] = -abs(particle["vel"][0])

            if particle["pos"][1] <= Y_MIN:
                particle["pos"][1] = Y_MIN
                particle["vel"][1] = abs(particle["vel"][1])
            elif particle["pos"][1] >= Y_MAX:
                particle["pos"][1] = Y_MAX
                particle["vel"][1] = -abs(particle["vel"][1])

    return positions


POSITIONS = simulate()
COLORS = np.array([particle["color"] for particle in PARTICLES], dtype=np.uint8)


def make_frame(t):
    frame_index = min(int(np.floor(t * FPS + 1e-9)), FRAME_COUNT - 1)
    frame = np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame[:] = BACKGROUND

    for pos, color in zip(POSITIONS[frame_index], COLORS):
        cx = int(np.floor(pos[0] + 1e-9))
        cy = int(np.floor(pos[1] + 1e-9))
        x0 = cx - HALF_SIZE
        y0 = cy - HALF_SIZE
        frame[y0 : y0 + SQUARE_SIZE, x0 : x0 + SQUARE_SIZE] = color

    return frame


def main():
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        "/app/output.mp4",
        fps=FPS,
        codec="libx264",
        audio=False,
        logger=None,
        ffmpeg_params=["-pix_fmt", "yuv420p"],
    )


if __name__ == "__main__":
    main()
