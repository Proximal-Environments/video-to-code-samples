"""Recreate the morphing balls animation using MoviePy and numpy."""
import numpy as np
from moviepy import VideoClip


WIDTH = 480
HEIGHT = 360
FPS = 24
DURATION = 20.0

BG_RGB = np.array([19, 9, 29], dtype=np.uint8)

# Ball positions and colors (RGB)
BALLS = [
    (65.5, 179.5, (254, 127, 0)),   # orange
    (181.0, 180.0, (128, 128, 128)),  # gray
    (297.5, 179.5, (254, 127, 0)),   # orange
    (415.5, 179.5, (0, 0, 254)),     # blue
]

BASE_R = 25.5  # base shape half-extent


def smoothstep(t):
    """Smooth 0->1 transition with zero derivative at ends."""
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def shape_params(frame_idx):
    """
    Compute superellipse exponent n and phase-4 (C, R) parameters
    for given frame. Total 20s = 480 frames split into four 120-frame quarters.
    """
    t = frame_idx / FPS  # seconds
    if t < 5.0:
        # Phase 1: static circle (n=2, no disks)
        return 2.0, 0.0, 0.0
    elif t < 10.0:
        # Phase 2: morph circle -> square via superellipse n
        # Use 1/n linear: 1/n goes from 0.5 (circle) to 0 (square) linearly.
        u = (t - 5.0) / 5.0  # 0..1
        inv_n = 0.5 * (1.0 - u)
        if inv_n < 1.0 / 50.0:
            n = 50.0
        else:
            n = 1.0 / inv_n
        return n, 0.0, 0.0
    elif t < 16.0:
        # Phase 3: static square; morph starts at t=16s (frame 384).
        return 50.0, 0.0, 0.0
    else:
        # Phase 4: square + 4 corner disks. Morph from square to quatrefoil
        # over ~4 seconds with ease-out timing (quick start, slow finish).
        u = (t - 16.0) / 4.0  # 0..1
        u = max(0.0, min(1.0, u))
        u = 1.0 - (1.0 - u) ** 2  # ease-out quadratic
        C_start = 25.5
        C_end = 11.0
        R_end = 19.0
        C = C_start + (C_end - C_start) * u
        R = R_end * u
        return 50.0, C, R


def render_ball_mask(cx, cy, n, C, R, base_r=BASE_R):
    """Return a boolean mask (as float32) for one ball at center (cx, cy).

    A pixel (i, j) belongs to the shape iff the point (i, j) is inside the
    (superellipse base) UNION (four corner disks). Sample at integer pixel
    coords to get sharp edges that match the reference's rasterization.
    """
    margin = max(base_r, np.hypot(C, C) + R) + 2
    x0 = int(np.floor(cx - margin))
    x1 = int(np.ceil(cx + margin))
    y0 = int(np.floor(cy - margin))
    y1 = int(np.ceil(cy + margin))
    x0 = max(0, x0); x1 = min(WIDTH, x1)
    y0 = max(0, y0); y1 = min(HEIGHT, y1)
    if x0 >= x1 or y0 >= y1:
        return None, 0, 0, 0, 0

    xs = np.arange(x0, x1)
    ys = np.arange(y0, y1)
    dx = xs[None, :] - cx
    dy = ys[:, None] - cy

    if n >= 50:
        in_shape = (np.abs(dx) <= base_r) & (np.abs(dy) <= base_r)
    elif n == 2:
        in_shape = dx * dx + dy * dy <= base_r * base_r
    else:
        in_shape = np.abs(dx) ** n + np.abs(dy) ** n <= base_r ** n

    if R > 0:
        for sx in (-1, 1):
            for sy in (-1, 1):
                ddx = dx - sx * C
                ddy = dy - sy * C
                in_shape = in_shape | (ddx * ddx + ddy * ddy <= R * R)

    return in_shape.astype(np.float32), x0, y0, x1, y1


def make_frame(t):
    frame_idx = int(round(t * FPS))
    n, C, R = shape_params(frame_idx)
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    img[:] = BG_RGB.astype(np.float32)

    for cx, cy, color in BALLS:
        result = render_ball_mask(cx, cy, n, C, R)
        if result[0] is None:
            continue
        mask, x0, y0, x1, y1 = result
        sub = img[y0:y1, x0:x1]
        ball_color = np.array(color, dtype=np.float32)
        sub[:] = sub * (1 - mask[:, :, None]) + ball_color * mask[:, :, None]
        img[y0:y1, x0:x1] = sub

    return np.clip(img, 0, 255).astype(np.uint8)


def main():
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        "/app/output.mp4",
        fps=FPS,
        codec="libx264",
        audio=False,
        logger=None,
    )


if __name__ == "__main__":
    main()
