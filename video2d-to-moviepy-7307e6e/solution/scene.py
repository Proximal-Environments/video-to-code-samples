"""Central circle + 6 satellites, 3-phase orbit animation."""
from moviepy import VideoClip
import numpy as np
from PIL import Image, ImageDraw
import math

def clamp(v, lo, hi): return max(lo, min(hi, v))
W, H, FPS, DUR = 480, 360, 24, 15.0
BG = (15, 15, 30)
N = 6
COLORS = [(255, 128, 0), (255, 128, 0), (128, 0, 255), (0, 255, 0), (255, 0, 255), (128, 0, 255), (128, 128, 128)]
RADII = [80, 120, 80, 100, 60, 80]
SPEEDS = [1.0, 0.25, 0.5, 0.5, 0.5, 1.0]
SAT_SIZES = [10, 10, 15, 15, 10, 15]
CENTER_R = 25
M = 40
CX, CY = W // 2, H // 2

def make_frame(t):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    progress = t / DUR
    if progress < 0.25:
        b12, b23 = 0.0, 0.0
    elif progress < 0.5:
        b12, b23 = (progress - 0.25) / 0.25, 0.0
    elif progress < 0.75:
        b12, b23 = 1.0, 0.0
    else:
        b12, b23 = 1.0, (progress - 0.75) / 0.25
    draw.ellipse([CX - CENTER_R, CY - CENTER_R, CX + CENTER_R, CY + CENTER_R], fill=COLORS[0])
    for idx in range(N):
        r1 = RADII[idx]
        r2 = RADII[idx] + 20
        r3 = RADII[idx] - 10
        orbit_r = r1 * (1 - b12) + r2 * b12 * (1 - b23) + max(20, r3) * b23
        for ring_pt in range(40):
            ra = ring_pt * 2 * math.pi / 40
            rx = int(CX + orbit_r * math.cos(ra))
            ry = int(CY + orbit_r * math.sin(ra))
            if M <= rx <= W - M and M <= ry <= H - M:
                img.putpixel((rx, ry), (50, 50, 50))
        dir1 = 1
        dir2 = 1
        dir3 = -1
        direction = dir1 * (1 - b12) + dir2 * b12 * (1 - b23) + dir3 * b23
        angle = direction * SPEEDS[idx] * t + idx * 2 * math.pi / N
        sx = int(CX + orbit_r * math.cos(angle))
        sy = int(CY + orbit_r * math.sin(angle))
        sx = clamp(sx, M, W - M)
        sy = clamp(sy, M, H - M)
        r = SAT_SIZES[idx]
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=COLORS[idx + 1])
    return np.array(img)

def main():
    clip = VideoClip(make_frame, duration=DUR).with_fps(FPS)
    clip.write_videofile("/app/output.mp4", codec="libx264", audio=False, logger=None)

if __name__ == "__main__":
    main()
