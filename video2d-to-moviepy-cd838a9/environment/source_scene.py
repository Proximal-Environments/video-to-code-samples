"""4 shapes morphing: circle → square → diamond."""
from moviepy import VideoClip
import numpy as np
from PIL import Image, ImageDraw
import math

def clamp(v, lo, hi): return max(lo, min(hi, v))
W, H, FPS, DUR = 480, 360, 24, 20.0
BG = (20, 10, 30)
N = 4
COLORS = [(255, 128, 0), (128, 128, 128), (255, 128, 0), (0, 0, 255)]
SIZE = 25
M = 40
N_PTS = 32

def morph_shape(cx, cy, size, morph1, morph2):
    pts = []
    for i in range(N_PTS):
        angle = i * 2 * math.pi / N_PTS
        ca, sa = math.cos(angle), math.sin(angle)
        circle_x = cx + size * ca
        circle_y = cy + size * sa
        square_x = cx + size * clamp(ca * 2, -1, 1)
        square_y = cy + size * clamp(sa * 2, -1, 1)
        diamond_x = cx + size * (abs(ca) * ca + abs(sa) * (-sa if abs(sa) > abs(ca) else 0))
        diamond_y = cy + size * (abs(sa) * sa + abs(ca) * (-ca if abs(ca) > abs(sa) else 0))
        diamond_x = cx + size * ca * (abs(ca) + abs(sa))
        diamond_y = cy + size * sa * (abs(ca) + abs(sa))
        x = circle_x * (1 - morph1) + square_x * morph1 * (1 - morph2) + diamond_x * morph2
        y = circle_y * (1 - morph1) + square_y * morph1 * (1 - morph2) + diamond_y * morph2
        pts.append((int(clamp(x, M, W - M)), int(clamp(y, M, H - M))))
    return pts

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
    for idx in range(N):
        cx = M + SIZE + idx * (W - 2 * M - 2 * SIZE) // max(1, N - 1)
        cy = H // 2
        pts = morph_shape(cx, cy, SIZE, b12, b23)
        draw.polygon(pts, fill=COLORS[idx])
    return np.array(img)

def main():
    clip = VideoClip(make_frame, duration=DUR).with_fps(FPS)
    clip.write_videofile("/app/output.mp4", codec="libx264", audio=False, logger=None)

if __name__ == "__main__":
    main()
