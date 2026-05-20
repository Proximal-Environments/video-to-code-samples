"""Solar-system style animation: 6 planets orbit a sun with expanding/contracting orbits."""
from moviepy import VideoClip
import numpy as np
import cv2


W, H = 480, 360
CX, CY = 240, 180
DURATION = 15.0
FPS = 24

BG_BGR = (28, 13, 14)
RING_BGR = (62, 47, 48)

PHASE_A = 3.75   # baseline radii
PHASE_B = 7.5    # ramp up
PHASE_C = 11.25  # peak radii
DELTA_R = 20.0
SHRINK_R = 28.0  # additional shrink past baseline in phase 4

PLANETS = [
    # name, BGR color, particle radius, base orbit radius, omega (deg/frame, negative=clockwise), initial theta (degrees)
    ("orange_p", (0, 127, 254), 10.45, 80.0, -2.388, 0.0),
    ("green",    (0, 254, 0),   15.44, 80.0, -1.198, -120.10),
    ("magenta",  (253, 0, 254), 15.58, 100.0, -1.190, 180.0),
    ("gray",     (128, 128, 128), 15.44, 80.0, -2.395, 60.26),
    ("purple_i", (254, 0, 128), 10.87, 60.0, -1.213, 120.96),
    ("purple_o", (254, 0, 128), 10.87, 120.0, -0.598, -59.70),
]

UNIQUE_RADII = [60.0, 80.0, 100.0, 120.0]
DOT_ANGLES_DEG = np.arange(0, 360, 9.0)  # 40 dots per ring


def orbit_radius(r_base, t):
    if t <= PHASE_A:
        return r_base
    if t <= PHASE_B:
        return r_base + DELTA_R * (t - PHASE_A) / (PHASE_B - PHASE_A)
    if t <= PHASE_C:
        return r_base + DELTA_R
    # Phase 4: shrink from r_base + DELTA_R down to r_base - (SHRINK_R - DELTA_R)
    return r_base + DELTA_R - SHRINK_R * (t - PHASE_C) / (DURATION - PHASE_C)


def planet_angle_deg(omega_per_frame, theta0_deg, t):
    f = t * FPS
    if f <= 270:
        return theta0_deg + omega_per_frame * f
    theta_at_270 = theta0_deg + omega_per_frame * 270.0
    df = f - 270.0
    K0 = 5.0
    K1 = 9.0
    # K linearly grows from K0 to K1 over 90 frames
    # angular velocity in phase 4 (in deg/frame): -omega_per_frame * (K0 + (K1-K0)*df/90)
    # integrate: delta = -omega_per_frame * (K0*df + 0.5*(K1-K0)/90 * df^2)
    growth = (K1 - K0) / 90.0
    delta = -omega_per_frame * (K0 * df + 0.5 * growth * df * df)
    return theta_at_270 + delta


SHIFT = 4
SCALE = 1 << SHIFT


def _circle(img, x, y, r, color):
    cv2.circle(img, (int(round(x * SCALE)), int(round(y * SCALE))),
               int(round(r * SCALE)), color, -1,
               lineType=cv2.LINE_AA, shift=SHIFT)


def make_frame(t):
    img = np.full((H, W, 3), BG_BGR, dtype=np.uint8)

    # Orbit rings (dotted)
    for r_base in UNIQUE_RADII:
        r_now = orbit_radius(r_base, t)
        for ang_deg in DOT_ANGLES_DEG:
            ang = np.radians(ang_deg)
            x = CX + r_now * np.cos(ang)
            y = CY - r_now * np.sin(ang)
            xi = int(round(x))
            yi = int(round(y))
            if 0 <= xi < W and 0 <= yi < H:
                img[yi, xi] = RING_BGR

    # Sun
    _circle(img, CX, CY, 25.3, (0, 127, 254))

    # Planets
    for name, color, p_size, r_base, omega, theta0 in PLANETS:
        r_orbit = orbit_radius(r_base, t)
        theta_deg = planet_angle_deg(omega, theta0, t)
        theta = np.radians(theta_deg)
        px = CX + r_orbit * np.cos(theta)
        py = CY - r_orbit * np.sin(theta)
        _circle(img, px, py, p_size, color)

    # cv2 uses BGR; moviepy expects RGB
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def main():
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile("/app/output.mp4", fps=FPS, logger=None, codec="libx264")


if __name__ == "__main__":
    main()
