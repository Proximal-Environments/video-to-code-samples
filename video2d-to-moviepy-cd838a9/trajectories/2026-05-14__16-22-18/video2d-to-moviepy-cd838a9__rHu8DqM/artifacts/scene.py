"""Animation matching reference.mp4 using algorithmic shape generation."""
from moviepy import VideoClip
import numpy as np

W, H = 480, 360
FPS = 24
DURATION = 20.0
TOTAL_FRAMES = 480

BG = np.array([19, 9, 29], dtype=np.float32)
ORANGE = np.array([255, 127, 0], dtype=np.float32)
GRAY = np.array([128, 128, 128], dtype=np.float32)
BLUE = np.array([0, 0, 255], dtype=np.float32)

# Number of theta samples for polar profile
N_THETA = 72  # every 5 degrees

# Phase 4 final polar profiles per shape (sampled at 5-degree intervals from 0 to 360 degrees).
# Derived by visual analysis of reference frame 479. Each value is r at angle i*5 degrees.
PROFILE_0 = np.array([
    26.00, 27.10, 29.40, 31.00, 32.90, 33.10, 34.60, 34.10, 35.20, 36.00,
    34.50, 34.70, 32.90, 32.50, 31.30, 29.50, 28.90, 26.60, 25.50, 26.60,
    28.90, 29.50, 31.30, 32.50, 32.90, 34.70, 34.50, 35.30, 32.60, 30.50,
    28.80, 27.50, 26.60, 25.80, 25.30, 25.00, 25.00, 25.00, 25.30, 25.80,
    26.60, 27.50, 28.80, 30.50, 32.60, 35.30, 34.50, 34.80, 34.00, 33.60,
    32.40, 30.50, 29.90, 27.60, 25.50, 26.60, 29.90, 30.50, 32.40, 33.60,
    34.00, 34.80, 35.70, 36.00, 35.20, 35.40, 34.60, 34.20, 31.90, 31.00,
    28.40, 27.10,
])
PROFILE_1 = np.array([
    26.00, 27.10, 29.40, 31.00, 32.90, 33.10, 34.60, 34.10, 35.20, 36.00,
    34.50, 34.70, 32.90, 32.50, 31.30, 29.50, 28.90, 26.60, 25.50, 26.60,
    28.90, 29.50, 31.30, 32.50, 32.90, 34.70, 34.50, 35.30, 35.00, 34.10,
    34.60, 33.10, 32.90, 31.00, 29.40, 27.10, 25.00, 26.00, 28.40, 31.00,
    31.90, 34.20, 34.60, 35.40, 35.20, 35.30, 34.50, 34.80, 34.00, 33.60,
    32.40, 30.50, 29.90, 27.60, 25.50, 26.60, 29.90, 30.50, 32.40, 33.60,
    34.00, 34.80, 35.70, 36.00, 35.20, 35.40, 34.60, 34.20, 31.90, 31.00,
    28.40, 27.10,
])
PROFILE_2 = np.array([
    26.00, 27.10, 29.40, 31.00, 32.90, 33.10, 34.60, 34.10, 35.20, 36.00,
    34.50, 34.70, 32.90, 32.50, 31.30, 29.50, 28.90, 26.60, 25.50, 26.60,
    28.90, 29.50, 31.30, 32.50, 32.90, 34.70, 34.50, 35.30, 35.00, 34.10,
    34.60, 33.10, 32.90, 31.00, 29.40, 27.10, 25.00, 26.00, 28.40, 31.00,
    31.90, 34.20, 34.60, 35.40, 35.20, 35.30, 34.50, 34.80, 34.00, 33.60,
    32.40, 30.50, 29.90, 27.60, 25.50, 26.60, 29.90, 30.50, 32.40, 33.60,
    34.00, 34.80, 35.70, 36.00, 35.20, 35.40, 34.60, 34.20, 31.90, 31.00,
    28.40, 27.10,
])
PROFILE_3 = np.array([
    26.00, 26.00, 26.40, 26.90, 27.60, 28.60, 30.00, 31.70, 33.90, 35.30,
    35.70, 33.50, 34.00, 32.50, 31.30, 29.50, 27.90, 25.50, 25.50, 27.60,
    27.90, 30.50, 31.30, 32.50, 34.00, 33.50, 35.70, 35.30, 35.20, 34.10,
    33.40, 34.20, 32.90, 30.00, 29.40, 27.10, 25.00, 26.00, 29.40, 30.00,
    32.90, 34.20, 34.60, 35.40, 35.20, 35.30, 34.50, 34.70, 34.00, 33.60,
    32.40, 31.50, 28.90, 26.60, 26.50, 26.60, 28.90, 30.50, 32.40, 33.60,
    34.00, 34.70, 35.70, 35.30, 33.90, 31.70, 30.00, 28.60, 27.60, 26.90,
    26.40, 26.00,
])

PROFILES = [PROFILE_0, PROFILE_1, PROFILE_2, PROFILE_3]
assert all(len(p) == N_THETA for p in PROFILES)

SHAPES = [
    {'cx': 64.5, 'cy': 180.0, 'R': 26.0, 'color': ORANGE, 'profile': PROFILE_0},
    {'cx': 180.5, 'cy': 180.0, 'R': 25.5, 'color': GRAY, 'profile': PROFILE_1},
    {'cx': 297.5, 'cy': 180.0, 'R': 26.0, 'color': ORANGE, 'profile': PROFILE_2},
    {'cx': 414.5, 'cy': 180.0, 'R': 26.0, 'color': BLUE, 'profile': PROFILE_3},
]

SS = 3
H_SS = H * SS
W_SS = W * SS


def smoothstep(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def lookup_profile(theta, profile):
    """Linearly interpolate polar profile at angles theta (in radians, can be negative)."""
    # Normalize theta to [0, 2*pi)
    t = (theta / (2 * np.pi)) * N_THETA  # in [0, N_THETA)
    t = t % N_THETA
    i0 = np.floor(t).astype(int)
    i1 = (i0 + 1) % N_THETA
    frac = t - i0
    return profile[i0] * (1 - frac) + profile[i1] * frac


def shape_radius(theta, shape, frame_n):
    R = shape['R']
    profile = shape['profile']
    if frame_n < 120:
        n_param = 2.0
        t4 = 0.0
    elif frame_n < 240:
        # Phase 2: morph circle->square. Use 1/n linear morph.
        u = (frame_n - 120) / 120
        # 1/n goes from 0.5 (n=2) to 0 (n=inf) linearly
        inv_n = 0.5 * (1 - u)
        if inv_n < 0.01:
            n_param = 100.0
        else:
            n_param = 1.0 / inv_n
        t4 = 0.0
    elif frame_n < 360:
        n_param = 100.0
        t4 = 0.0
    else:
        # Phase 4: morph square->flower. Piecewise easing based on reference area data.
        u = (frame_n - 360) / 116
        u = min(1.0, u)
        # Reference morph: gentle middle, with snap at end.
        # Piecewise linear approx: u-> t4
        # (0, 0), (0.2, 0.11), (0.83, 0.56), (1.0, 1.0)
        if u < 0.2:
            t4 = u / 0.2 * 0.11
        elif u < 0.83:
            t4 = 0.11 + (u - 0.2) / 0.63 * 0.45
        else:
            t4 = 0.56 + (u - 0.83) / 0.17 * 0.44
        n_param = 100.0

    # Superellipse polar radius (square when n large)
    c = np.abs(np.cos(theta))
    s = np.abs(np.sin(theta))
    if n_param >= 50:
        denom = np.maximum(c, s)
    else:
        denom = (c**n_param + s**n_param)**(1.0 / n_param)
    denom = np.maximum(denom, 1e-9)
    r_super = R / denom

    if t4 > 0:
        r_profile = lookup_profile(theta, profile)
        return (1 - t4) * r_super + t4 * r_profile
    else:
        return r_super


def render_shape(buf, shape, frame_n):
    cx, cy = shape['cx'], shape['cy']
    color = shape['color']

    R_max = 40 + 2
    cx_ss = cx * SS
    cy_ss = cy * SS
    R_max_ss = R_max * SS
    x_min = max(0, int(cx_ss - R_max_ss))
    x_max = min(W_SS, int(cx_ss + R_max_ss + 1))
    y_min = max(0, int(cy_ss - R_max_ss))
    y_max = min(H_SS, int(cy_ss + R_max_ss + 1))

    xs = (np.arange(x_min, x_max).reshape(1, -1) + 0.5 - cx_ss) / SS
    ys = (np.arange(y_min, y_max).reshape(-1, 1) + 0.5 - cy_ss) / SS

    r_pix = np.sqrt(xs * xs + ys * ys)
    theta = np.arctan2(ys, xs)

    r_target = shape_radius(theta, shape, frame_n)
    mask = r_pix <= r_target

    buf_region = buf[y_min:y_max, x_min:x_max]
    buf_region[mask] = color


def make_frame(t):
    frame_n = int(round(t * FPS))
    img_ss = np.empty((H_SS, W_SS, 3), dtype=np.float32)
    img_ss[..., :] = BG
    for shape in SHAPES:
        render_shape(img_ss, shape, frame_n)
    img = img_ss.reshape(H, SS, W, SS, 3).mean(axis=(1, 3))
    return np.clip(img, 0, 255).astype(np.uint8)


def main():
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile("/app/output.mp4", fps=FPS, logger=None,
                         codec="libx264", preset="medium")


if __name__ == "__main__":
    main()
