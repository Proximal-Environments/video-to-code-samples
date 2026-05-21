# Bouncing Squares with Shrinking Walls in Revideo

> Reproduce a reference animation of 12 colored squares bouncing inside walls that shrink and recover across phases. The agent writes a Revideo TypeScript scene using algorithmic physics and renders it to match the reference video.

---

## Task Configuration

| Property | Value |
|----------|-------|
| Difficulty | hard |
| Category | animation |
| Agent Timeout | 7200s |
| Verifier Timeout | 1200s |
| Internet Access | Enabled |
| CPUs / Memory | 8 / 32768 MB |

> **Why `allow_internet = true`?** Revideo renders via Puppeteer controlling a headless Chromium instance over localhost. Harbor's `allow_internet = false` applies `network_mode: none`, which kills all networking including loopback — Puppeteer cannot connect to Chromium and rendering fails. The agent does not need external internet; only localhost communication between Puppeteer and Chromium is used.

---

<!-- BEGIN:ROLLOUT_RESULTS -->
## Rollout Results

### Overview

| Metric | Value |
|--------|-------|
| Trials | 6 (6 scoreable) |
| Models tested | 2 |
| Success rate | 0/6 (0%) |
| Mean reward | 0.0 |
| Reward range | 0.0 – 0.0 |
| Total agent cost | $0.00 |
| Post-QA cost | $10.34 |
| Oracle reward | 1.0 |

### Performance by Model

| Model | Trials | Success Rate | Mean Reward | Mean Time | Mean Cost |
|-------|--------|--------------|-------------|-----------|-----------|
| claude-opus-4-7 | 3/3 | 0/3 (0%) | 0.0 | 22m | $0.00 |
| gpt-5.4 | 3/3 | 0/3 (0%) | 0.0 | 30m | $0.00 |
| **Overall** | **6/6** | **0/6 (0%)** | **0.0** | | **$0.00** |

### Trial Details

#### claude-opus-4-7

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| 2zdn5TV | 0.0 | 46m | $0.00 | zero_reward | Extract frames, detect colors, estimate velocities, build physics sim in Revideo |
| CUDhFhi | 0.0 | 7m | $0.00 | zero_reward | Extract frames, analyze colors/positions/velocities, implement simple bounce physics in Revideo |
| fd4sQ7h | 0.0 | 12m | $0.00 | zero_reward | Extract frame positions via Python tracking, build physics sim in Revideo |

#### gpt-5.4

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| SoHsTa8 | 0.0 | 16m | $0.00 | anti_cheat_penalty | Extract frame positions via template matching, encode as DCT coefficients, decode at runtime |
| mXZfe26 | 0.0 | 24m | $0.00 | anti_cheat_penalty | OpenCV frame tracking, compress trajectories into piecewise velocity segments |
| zLMYrH9 | 0.0 | 49m | $0.00 | anti_cheat_penalty | Extract per-frame positions via DCT, encode as base64, reconstruct via cosine series |

### Post-Rollout QA

| Check | Result |
|-------|--------|
| Trial verdicts | 6/6 FAIR |

<!-- END:ROLLOUT_RESULTS -->
