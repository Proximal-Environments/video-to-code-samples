I have a reference animation `reference.mp4`. Write `scene.py` using MoviePy primitives (`ColorClip`, `ImageClip`, `CompositeVideoClip`, numpy frame generation, etc.). Your code must be self-contained in `scene.py`.

Use algorithmic approaches — mathematical formulas, physics equations, parametric curves, easing functions, etc. Do not extract and hardcode per-frame position data from the reference video.

Run with `uv run python scene.py`. The rendered `output.mp4` must match `reference.mp4` exactly.

Keep `scene.py` valid and rendering throughout your iteration; your sandbox times out in 2 hours.

Available at `/app/`:
- `reference.mp4` — the target animation
- `scene.py` — your MoviePy source (write here)
- Pre-installed: `moviepy`, `pillow`, `opencv`, `scikit-image`, `numpy`, `ffmpeg`, `ffprobe`
