I have a reference animation `reference.mp4`. Write a Revideo scene in `src/project.tsx` that reproduces it.

Use algorithmic approaches — mathematical formulas, physics equations, parametric curves, easing functions, etc. Do not extract and hardcode per-frame position data from the reference video.

Render with `npm run render`. The rendered `output/video.mp4` must match `reference.mp4`.

Keep `src/project.tsx` valid and rendering throughout your iteration; your sandbox times out in 2 hours.

Available at `/app/`:
- `reference.mp4` — the target animation
- `src/project.tsx` — your Revideo source (write here)
- `src/render.ts` — render script (already configured)
- Pre-installed: `@revideo/core`, `@revideo/2d`, `@revideo/renderer`, Chromium, `ffmpeg`, `ffprobe`