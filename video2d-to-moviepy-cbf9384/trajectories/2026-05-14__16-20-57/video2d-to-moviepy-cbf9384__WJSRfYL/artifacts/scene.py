"""Bouncing-square animation rendered with MoviePy."""
import numpy as np
from moviepy import VideoClip

W, H = 480, 360
FPS = 24
DURATION = 18.0
NUM_FRAMES = int(round(DURATION * FPS))

BG = (9, 19, 25)
SIZE = 11
HALF = SIZE // 2

WALL_X_LO, WALL_X_HI = 45.0, 435.0
WALL_Y_LO, WALL_Y_HI = 45.0, 315.0

BALLS = [
    # (x0, y0, vx, vy, color_rgb)
    (60.0,  60.0,  25/12, -5/4, (255, 0, 0)),
    (180.0, 60.0,  -5/3,   5/4, (255, 125, 0)),
    (300.0, 60.0,  -5/3,  25/24, (255, 252, 255)),
    (420.0, 60.0,  25/12, -5/3, (0, 255, 255)),
    (60.0,  180.0, 25/12,  5/4, (126, 126, 123)),
    (180.0, 180.0, 5/4,    5/3, (255, 254, 0)),
    (300.0, 180.0, 5/3,   -5/4, (0, 251, 255)),
    (420.0, 180.0, -5/4,   5/3, (0, 255, 0)),
    (60.0,  300.0, -5/3,   25/24, (252, 253, 0)),
    (180.0, 300.0, -5/3,   25/24, (129, 129, 126)),
    (300.0, 300.0, -5/4,  -5/4, (0, 255, 0)),
    (420.0, 300.0, -5/4,  -5/3, (129, 129, 126)),
]


def simulate():
    """Return positions[frame][ball] = (cx_int, cy_int)."""
    state = [(x, y, vx, vy) for (x, y, vx, vy, _) in BALLS]
    frames = []
    for f in range(NUM_FRAMES):
        positions = [(int(s[0]), int(s[1])) for s in state]
        frames.append(positions)
        new_state = []
        for (x, y, vx, vy) in state:
            x += vx
            if x < WALL_X_LO:
                x = WALL_X_LO
                vx = -vx
            elif x > WALL_X_HI:
                x = WALL_X_HI
                vx = -vx
            y += vy
            if y < WALL_Y_LO:
                y = WALL_Y_LO
                vy = -vy
            elif y > WALL_Y_HI:
                y = WALL_Y_HI
                vy = -vy
            new_state.append((x, y, vx, vy))
        state = new_state
    return frames


def main():
    positions_by_frame = simulate()
    bg = np.array(BG, dtype=np.uint8)
    colors = [b[4] for b in BALLS]

    def make_frame(t):
        idx = int(round(t * FPS))
        if idx >= NUM_FRAMES:
            idx = NUM_FRAMES - 1
        img = np.empty((H, W, 3), dtype=np.uint8)
        img[:] = bg
        for (cx, cy), col in zip(positions_by_frame[idx], colors):
            x0 = cx - HALF
            y0 = cy - HALF
            img[y0:y0 + SIZE, x0:x0 + SIZE] = col
        return img

    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile("/app/output.mp4", fps=FPS, logger=None, codec="libx264")


if __name__ == "__main__":
    main()
