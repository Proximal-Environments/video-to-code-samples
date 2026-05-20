"""Solar-system style animation: 6 planets orbit a sun, with a shared
time-warp that reverses near the end of the clip and a piecewise-linear
radial pulse shared by all planets."""
from moviepy import *
import numpy as np

W, H = 480, 360
FPS = 24
DURATION = 15.0
NFRAMES = int(round(FPS * DURATION))  # 360
CX, CY = 240.0, 180.0
BG = (14, 13, 30)

# Sun: (color, draw_radius)
SUN_COLOR = (255, 128, 0)
SUN_R = 25

# Planet specs: (color, draw_radius, R_max, intrinsic_omega, theta_0)
# r(t) = R_max - 30 + 30 * r_norm(t)  (radial pulse spans 30 px, lands on R_max at peak)
PLANETS = [
    # inner purple
    ((128, 0, 255), 10,  79.83, -0.020478,  2.1055),
    # small orange
    ((255, 128, 0), 10,  99.91, -0.040880,  0.0133),
    # gray
    ((128, 128, 128), 15,  99.85, -0.040891,  1.0620),
    # green
    ((  0, 255,   0), 15, 100.04, -0.020426, -2.0883),
    # magenta
    ((255,   0, 255), 15, 120.06, -0.020442, -3.1342),
    # outer purple
    ((128,   0, 255), 10, 140.04, -0.010228, -1.0459),
]

# Time-warping shared across all planets.
T1 = 270.0
PHASE1_K = 1.0206
PHASE1_C = -0.583
ALPHA = 4.7917
HALF_BETA = 0.0252

def tau(t):
    """Shared time-warp: linear forward, quadratic deceleration in reverse."""
    if t < T1:
        return PHASE1_K * t + PHASE1_C
    s = t - T1
    return (PHASE1_K * T1 + PHASE1_C) - ALPHA * s - HALF_BETA * s * s


# Radial pulse: r_norm(t) goes 1/3 -> 1 (climb 90..180) -> 1 (plateau 180..270) -> 0 (drop 270..360)
def r_norm(t):
    if t < 90.0:
        return 1.0 / 3.0
    if t < 180.0:
        return 1.0 / 3.0 + (2.0 / 3.0) * (t - 90.0) / 90.0
    if t < 270.0:
        return 1.0
    return max(0.0, 1.0 - (t - 270.0) / 90.0)


def fill_disc(canvas, cx, cy, radius, color):
    """Anti-aliased disc, blended with current canvas contents."""
    h, w = canvas.shape[:2]
    x0 = max(0, int(np.floor(cx - radius - 1)))
    x1 = min(w, int(np.ceil(cx + radius + 1)))
    y0 = max(0, int(np.floor(cy - radius - 1)))
    y1 = min(h, int(np.ceil(cy + radius + 1)))
    if x0 >= x1 or y0 >= y1:
        return
    ys = np.arange(y0, y1)[:, None]
    xs = np.arange(x0, x1)[None, :]
    dist = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
    # smooth 1-pixel edge: 1 inside, 0 outside, linear in [radius-0.5, radius+0.5]
    alpha = np.clip(radius + 0.5 - dist, 0.0, 1.0)
    region = canvas[y0:y1, x0:x1].astype(np.float32)
    color_arr = np.array(color, dtype=np.float32)
    blended = region * (1.0 - alpha[..., None]) + color_arr * alpha[..., None]
    canvas[y0:y1, x0:x1] = np.clip(blended, 0, 255).astype(np.uint8)


def planet_position(f, R_max, omega, th0):
    tt = tau(f)
    rn = r_norm(f)
    R = R_max - 30.0 + 30.0 * rn
    theta = th0 + omega * tt
    x = CX + R * np.cos(theta)
    y = CY - R * np.sin(theta)
    return x, y


def make_frame(t_sec):
    f = t_sec * FPS  # fractional frame index 0..NFRAMES
    canvas = np.empty((H, W, 3), dtype=np.uint8)
    canvas[..., 0] = BG[0]
    canvas[..., 1] = BG[1]
    canvas[..., 2] = BG[2]

    # Sun
    fill_disc(canvas, CX, CY, SUN_R, SUN_COLOR)

    # Planets (current positions)
    for col, pr, R_max, omega, th0 in PLANETS:
        x, y = planet_position(f, R_max, omega, th0)
        fill_disc(canvas, x, y, pr, col)

    return canvas


def main():
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        "/app/output.mp4", fps=FPS, logger=None,
        codec="libx264", preset="ultrafast",
        ffmpeg_params=["-pix_fmt", "yuv420p"],
    )


if __name__ == "__main__":
    main()
