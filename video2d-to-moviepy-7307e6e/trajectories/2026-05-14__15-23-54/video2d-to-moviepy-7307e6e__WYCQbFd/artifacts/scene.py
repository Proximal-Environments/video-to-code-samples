"""Solar system animation with breathing orbits."""
import math
import numpy as np
import cv2
from moviepy import VideoClip


WIDTH, HEIGHT = 480, 360
FPS = 24
N_FRAMES = 360
DURATION = N_FRAMES / FPS

CX, CY = 240, 180
BG_BGR = (30, 13, 14)  # dark navy

# Orbital angular velocity baseline is 1 rad/second.
OMEGA_FAST = 1.0 / FPS
OMEGA_MED  = 0.5 / FPS
OMEGA_SLOW = 0.25 / FPS

# planets: (orbit_radius, theta0_rad, omega_rad_per_frame, body_radius_px, color_bgr)
PLANETS = [
    (80,                0.0, OMEGA_FAST, 10,  (  0, 127, 255)),  # small orange
    (100,         math.pi, OMEGA_MED,  15,  (255,   0, 255)),  # magenta
    (80,    2*math.pi/3,   OMEGA_MED,  15,  (  0, 255,   0)),  # green
    (60,   -2*math.pi/3,   OMEGA_MED,  11,  (255,   0, 128)),  # violet inner
    (120,         math.pi/3, OMEGA_SLOW, 11,  (255,   0, 128)),  # violet outer
    (80,       -math.pi/3, OMEGA_FAST, 15,  (128, 128, 128)),  # gray (drawn last)
]
SUN_RADIUS = 25
SUN_COLOR  = (0, 127, 255)

RING_RADII = (60, 80, 100, 120)
DOTS_PER_RING = 40
DOT_COLOR = (50, 49, 64)


def psi(frame: float) -> float:
    if frame <= 270.0:
        return frame
    dt = frame - 270.0
    return 270.0 - 5.0 * dt - 0.022 * dt * dt - 1.5e-6 * dt * dt * dt


def delta_r(frame: float) -> float:
    if frame <= 90.0:
        return 0.0
    if frame <= 180.0:
        return 20.0 * (frame - 90.0) / 90.0
    if frame <= 270.0:
        return 20.0
    return 20.0 - 0.34 * (frame - 270.0)


def _precompute_ring_dots():
    pts = []
    for ring_r in RING_RADII:
        for k in range(DOTS_PER_RING):
            angle = (2.0 * math.pi * k) / DOTS_PER_RING - math.pi
            x = CX + ring_r * math.cos(angle)
            y = CY + ring_r * math.sin(angle)
            pts.append((int(x), int(y)))
    return pts


RING_DOTS = _precompute_ring_dots()


def make_frame(t_seconds: float) -> np.ndarray:
    img = np.full((HEIGHT, WIDTH, 3), BG_BGR, dtype=np.uint8)

    for x, y in RING_DOTS:
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            img[y, x] = DOT_COLOR

    frame = t_seconds * FPS
    phase = psi(frame)
    dr = delta_r(frame)

    for r0, theta0, omega, body_r, color in PLANETS:
        r = r0 + dr
        a = theta0 + omega * phase
        x = int(CX + r * math.cos(a))
        y = int(CY + r * math.sin(a))
        cv2.circle(img, (x, y), body_r, color, thickness=-1, lineType=cv2.LINE_AA)

    cv2.circle(img, (CX, CY), SUN_RADIUS, SUN_COLOR,
               thickness=-1, lineType=cv2.LINE_AA)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def main():
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        "/app/output.mp4",
        fps=FPS,
        codec="libx264",
        preset="medium",
        audio=False,
        logger=None,
    )


if __name__ == "__main__":
    main()
