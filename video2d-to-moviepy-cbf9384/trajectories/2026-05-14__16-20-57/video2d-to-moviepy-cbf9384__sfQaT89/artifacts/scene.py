"""Bouncing squares animation. Recreated algorithmically from reference.mp4."""
from moviepy import VideoClip
import numpy as np

W, H = 480, 360
FPS = 24
DURATION = 18.0
SQ_SIZE = 12  # square side in pixels
HALF = SQ_SIZE / 2
BG = (9, 19, 25)

# Container walls (in center coordinates)
WALL_LEFT = 45.0
WALL_RIGHT = 435.0
WALL_TOP = 45.0
WALL_BOTTOM = 315.0

# Initial grid positions and colors (from reference frame 0)
INITIAL = [
    # (x, y, color, vx, vy)
    ( 60.0,  60.0, (255,   0,   0),  48, -48),  # red
    (180.0,  60.0, (255, 128,   0), -40,  30),  # orange
    (300.0,  60.0, (255, 255, 255), -40,  24),  # white
    (420.0,  60.0, (  0, 255, 255),  48, -48),  # cyan top-right
    ( 60.0, 180.0, (140, 145, 148),  50,  30),  # gray
    (180.0, 180.0, (255, 255,   0),  24,  36),  # yellow
    (300.0, 180.0, (  0, 255, 255),  40, -30),  # cyan mid
    (420.0, 180.0, (  0, 255,   0), -30,  40),  # green mid
    ( 60.0, 300.0, (255, 255,   0), -40,  25),  # yellow bot
    (180.0, 300.0, (140, 145, 148), -40,  25),  # gray bot mid
    (300.0, 300.0, (  0, 255,   0), -30, -30),  # green bot
    (420.0, 300.0, (140, 145, 148), -30, -42),  # gray bot right
]


def simulate():
    """Simulate the bouncing squares with elastic collisions, returning positions per frame."""
    N = len(INITIAL)
    positions = np.zeros((N, 2))
    velocities = np.zeros((N, 2))
    colors = []
    for i, (x, y, c, vx, vy) in enumerate(INITIAL):
        positions[i] = (x, y)
        velocities[i] = (vx, vy)
        colors.append(c)
    colors = np.array(colors, dtype=np.uint8)

    n_frames = int(DURATION * FPS)
    history = np.zeros((n_frames, N, 2))
    dt = 1.0 / FPS
    substeps = 8

    for f in range(n_frames):
        history[f] = positions
        # Sub-step for collision accuracy
        for _ in range(substeps):
            sdt = dt / substeps
            positions += velocities * sdt

            # Bounce off walls
            for i in range(N):
                if positions[i, 0] < WALL_LEFT:
                    positions[i, 0] = WALL_LEFT
                    velocities[i, 0] = abs(velocities[i, 0])
                elif positions[i, 0] > WALL_RIGHT:
                    positions[i, 0] = WALL_RIGHT
                    velocities[i, 0] = -abs(velocities[i, 0])
                if positions[i, 1] < WALL_TOP:
                    positions[i, 1] = WALL_TOP
                    velocities[i, 1] = abs(velocities[i, 1])
                elif positions[i, 1] > WALL_BOTTOM:
                    positions[i, 1] = WALL_BOTTOM
                    velocities[i, 1] = -abs(velocities[i, 1])

            # Pairwise elastic AABB collisions
            for i in range(N):
                for j in range(i + 1, N):
                    dx = positions[j, 0] - positions[i, 0]
                    dy = positions[j, 1] - positions[i, 1]
                    if abs(dx) < SQ_SIZE and abs(dy) < SQ_SIZE:
                        # Determine overlap axis
                        ox = SQ_SIZE - abs(dx)
                        oy = SQ_SIZE - abs(dy)
                        if ox < oy:
                            # x-axis collision
                            if velocities[i, 0] - velocities[j, 0] > 0 if dx > 0 else velocities[j, 0] - velocities[i, 0] > 0:
                                velocities[i, 0], velocities[j, 0] = velocities[j, 0], velocities[i, 0]
                            # Push apart
                            if dx > 0:
                                positions[i, 0] -= ox / 2
                                positions[j, 0] += ox / 2
                            else:
                                positions[i, 0] += ox / 2
                                positions[j, 0] -= ox / 2
                        else:
                            if (velocities[i, 1] - velocities[j, 1] > 0 if dy > 0 else velocities[j, 1] - velocities[i, 1] > 0):
                                velocities[i, 1], velocities[j, 1] = velocities[j, 1], velocities[i, 1]
                            if dy > 0:
                                positions[i, 1] -= oy / 2
                                positions[j, 1] += oy / 2
                            else:
                                positions[i, 1] += oy / 2
                                positions[j, 1] -= oy / 2
    return history, colors


def render_frame(positions, colors):
    """Render a single frame from positions and colors."""
    frame = np.full((H, W, 3), BG, dtype=np.float32)
    for (x, y), color in zip(positions, colors):
        lx, ly = x - HALF, y - HALF
        rx, ry = x + HALF, y + HALF
        i0 = max(0, int(np.floor(lx)))
        j0 = max(0, int(np.floor(ly)))
        i1 = min(W, int(np.ceil(rx)))
        j1 = min(H, int(np.ceil(ry)))
        if i1 <= i0 or j1 <= j0:
            continue
        xs = np.arange(i0, i1)
        ys = np.arange(j0, j1)
        cx = np.minimum(rx - xs, 1.0) - np.maximum(lx - xs, 0.0)
        cy = np.minimum(ry - ys, 1.0) - np.maximum(ly - ys, 0.0)
        cx = np.clip(cx, 0.0, 1.0)
        cy = np.clip(cy, 0.0, 1.0)
        alpha = cy[:, None] * cx[None, :]
        region = frame[j0:j1, i0:i1]
        fg = np.array(color, dtype=np.float32)
        frame[j0:j1, i0:i1] = alpha[..., None] * fg + (1 - alpha[..., None]) * region
    return frame.astype(np.uint8)


def main():
    history, colors = simulate()

    def make_frame(t):
        f = min(int(round(t * FPS)), history.shape[0] - 1)
        return render_frame(history[f], colors)

    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile("/app/output.mp4", fps=FPS, codec="libx264", logger=None)


if __name__ == "__main__":
    main()
