"""3x4 squares bouncing diagonally, walls shrink in phase 2."""
from moviepy import VideoClip
import numpy as np
from PIL import Image, ImageDraw
import math

def clamp(v, lo, hi): return max(lo, min(hi, v))
W, H, FPS, DUR = 480, 360, 24, 18.0
BG = (10, 20, 25)
ROWS, COLS = 3, 4
N = ROWS * COLS
COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 255), (0, 255, 255), (128, 128, 128), (255, 255, 0), (0, 255, 255), (0, 255, 0), (255, 255, 0), (128, 128, 128), (0, 255, 0), (128, 128, 128)]
VX = [50, -40, -40, 50, 50, 30, 40, -30, -40, -40, -30, -30]
VY = [-30, 30, 25, -40, 30, 40, -30, 40, 25, 25, -30, -40]
M = 40

def simulate(t, wall_shrink):
    dt = 1.0 / FPS
    steps = int(t * FPS)
    positions = []
    lw = M + wall_shrink
    rw = W - M - wall_shrink
    tw = M + wall_shrink
    bw = H - M - wall_shrink
    for idx in range(N):
        row = idx // COLS
        col = idx % COLS
        x = float(M + 20 + col * (W - 2 * M - 40) // max(1, COLS - 1))
        y = float(M + 20 + row * (H - 2 * M - 40) // max(1, ROWS - 1))
        vx = float(VX[idx])
        vy = float(VY[idx])
        for _ in range(steps):
            x += vx * dt
            y += vy * dt
            if x < lw + 5: x = float(lw + 5); vx = -vx
            elif x > rw - 5: x = float(rw - 5); vx = -vx
            if y < tw + 5: y = float(tw + 5); vy = -vy
            elif y > bw - 5: y = float(bw - 5); vy = -vy
        positions.append((int(x), int(y)))
    return positions

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
    shrink1 = 0
    shrink2 = 40
    shrink3 = 20
    shrink = int(shrink1 * (1 - b12) + shrink2 * b12 * (1 - b23) + shrink3 * b23)
    positions = simulate(t, shrink)
    for idx, (x, y) in enumerate(positions):
        draw.rectangle([x - 5, y - 5, x + 5, y + 5], fill=COLORS[idx])
    return np.array(img)

def main():
    clip = VideoClip(make_frame, duration=DUR).with_fps(FPS)
    clip.write_videofile("/app/output.mp4", codec="libx264", audio=False, logger=None)

if __name__ == "__main__":
    main()
