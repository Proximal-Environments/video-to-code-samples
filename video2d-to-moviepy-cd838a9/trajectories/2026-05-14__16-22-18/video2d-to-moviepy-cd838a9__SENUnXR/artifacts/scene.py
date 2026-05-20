from __future__ import annotations

import math

import numpy as np
from moviepy import VideoClip


WIDTH = 480
HEIGHT = 360
FPS = 24
DURATION = 20.0

BG_COLOR = np.array([19.0, 9.0, 29.0], dtype=np.float32)
COLORS = np.array(
    [
        [254.0, 127.0, 0.0],
        [128.0, 128.0, 128.0],
        [254.0, 127.0, 0.0],
        [0.0, 0.0, 254.0],
    ],
    dtype=np.float32,
)

# Centers measured from the reference; the blue shape sits a half pixel lower.
CENTERS = np.array(
    [
        [65.0, 180.0],
        [181.0, 180.0],
        [298.0, 180.0],
        [414.5, 180.5],
    ],
    dtype=np.float32,
)

PATCH = 88
SUPER = 4
PATCH_SS = PATCH * SUPER
PATCH_CENTER = (PATCH - 1) / 2.0
SHADOW_OFFSET = np.array([2.7, 2.7], dtype=np.float32)
SHADOW_BLUR = 1.7
SHADOW_OPACITY = 0.23
BASE_RADIUS = 25.0
FINAL_CLUSTER_OFFSET = 10.0
FINAL_CLUSTER_RADIUS = 21.4
YS_SS, XS_SS = np.mgrid[0:PATCH_SS, 0:PATCH_SS].astype(np.float32)
XX_SS = (XS_SS + 0.5) / SUPER - PATCH_CENTER
YY_SS = (YS_SS + 0.5) / SUPER - PATCH_CENTER


def smoothstep01(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def morph_params(t: float) -> tuple[str, float]:
    if t <= 122.0 / FPS:
        return "round", BASE_RADIUS
    if t <= 240.0 / FPS:
        u = smoothstep01((t - 122.0 / FPS) / ((240.0 - 122.0) / FPS))
        return "round", BASE_RADIUS * (1.0 - u)
    if t <= 360.0 / FPS:
        return "blend", 0.0
    u = smoothstep01((t - 360.0 / FPS) / ((479.0 - 360.0) / FPS))
    return "blend", u


def rounded_box_distance(xx: np.ndarray, yy: np.ndarray, radius: float) -> np.ndarray:
    inner = max(BASE_RADIUS - radius, 0.0)
    qx = np.abs(xx) - inner
    qy = np.abs(yy) - inner
    outside = np.hypot(np.maximum(qx, 0.0), np.maximum(qy, 0.0))
    inside = np.minimum(np.maximum(qx, qy), 0.0)
    return outside + inside - radius


def square_distance(xx: np.ndarray, yy: np.ndarray) -> np.ndarray:
    return np.maximum(np.abs(xx), np.abs(yy)) - BASE_RADIUS


def cluster_distance(xx: np.ndarray, yy: np.ndarray) -> np.ndarray:
    dist = np.full_like(xx, 1e9)
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            dx = xx - sx * FINAL_CLUSTER_OFFSET
            dy = yy - sy * FINAL_CLUSTER_OFFSET
            dist = np.minimum(dist, np.hypot(dx, dy) - FINAL_CLUSTER_RADIUS)
    return dist


def soft_alpha_from_distance(distance: np.ndarray, feather: float = 0.85) -> np.ndarray:
    return np.clip(0.5 - distance / feather, 0.0, 1.0)


def render_patch(t: float) -> tuple[np.ndarray, np.ndarray]:
    mode, amount = morph_params(t)
    if mode == "round":
        distance = rounded_box_distance(XX_SS, YY_SS, amount)
    else:
        square = square_distance(XX_SS, YY_SS)
        clusters = cluster_distance(XX_SS, YY_SS)
        distance = square * (1.0 - amount) + clusters * amount
    alpha_hi = soft_alpha_from_distance(distance)

    shadow_x = XX_SS - SHADOW_OFFSET[0]
    shadow_y = YY_SS - SHADOW_OFFSET[1]
    if mode == "round":
        shadow_distance = rounded_box_distance(shadow_x, shadow_y, amount)
    else:
        square = square_distance(shadow_x, shadow_y)
        clusters = cluster_distance(shadow_x, shadow_y)
        shadow_distance = square * (1.0 - amount) + clusters * amount
    shadow_hi = np.exp(-np.maximum(shadow_distance, 0.0) ** 2 / (2.0 * SHADOW_BLUR * SHADOW_BLUR))
    shadow_hi *= np.clip(0.5 - shadow_distance / 1.25, 0.0, 1.0) * SHADOW_OPACITY

    alpha = alpha_hi.reshape(PATCH, SUPER, PATCH, SUPER).mean(axis=(1, 3))
    shadow = shadow_hi.reshape(PATCH, SUPER, PATCH, SUPER).mean(axis=(1, 3))
    return alpha.astype(np.float32), shadow.astype(np.float32)


def composite_patch(
    frame: np.ndarray,
    patch_alpha: np.ndarray,
    patch_shadow: np.ndarray,
    color: np.ndarray,
    center_x: float,
    center_y: float,
) -> None:
    left = int(round(center_x - PATCH / 2))
    top = int(round(center_y - PATCH / 2))
    right = left + PATCH
    bottom = top + PATCH

    frame_region = frame[top:bottom, left:right]

    frame_region[:] = frame_region * (1.0 - patch_shadow[..., None])
    frame_region[:] = frame_region * (1.0 - patch_alpha[..., None]) + color * patch_alpha[..., None]


def make_frame(t: float) -> np.ndarray:
    frame = np.tile(BG_COLOR, (HEIGHT, WIDTH, 1))
    alpha, shadow = render_patch(t)
    for color, (cx, cy) in zip(COLORS, CENTERS):
        composite_patch(frame, alpha, shadow, color, float(cx), float(cy))
    return np.clip(frame, 0, 255).astype(np.uint8)


def main() -> None:
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        "/app/output.mp4",
        fps=FPS,
        codec="libx264",
        audio=False,
        preset="medium",
        logger=None,
    )


if __name__ == "__main__":
    main()
