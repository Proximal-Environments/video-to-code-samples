# Shape Morphing Animation in Revideo

> Reproduce a reference animation of 4 shapes morphing through circle, square, and diamond forms using Revideo. The agent writes a TypeScript scene file that algorithmically generates the animation to match the reference video.

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
| Success rate | 4/6 (67%) |
| Mean reward | 0.2027 |
| Reward range | 0.0 – 0.4904 |
| Total agent cost | $0.00 |
| Post-QA cost | $9.49 |
| Oracle reward | 1.0 |

### Performance by Model

| Model | Trials | Success Rate | Mean Reward | Mean Time | Mean Cost |
|-------|--------|--------------|-------------|-----------|-----------|
| claude-opus-4-7 | 3/3 | 3/3 (100%) | 0.3055 | 33m | $0.00 |
| gpt-5.4 | 3/3 | 1/3 (33%) | 0.0998 | 13m | $0.00 |
| **Overall** | **6/6** | **4/6 (67%)** | **0.2027** | | **$0.00** |

### Trial Details

#### claude-opus-4-7

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| 7UKtivx | 0.0875 | 43m | $0.00 | below_threshold | Algorithmic Rect morph via Revideo smoothCorners and cornerSharpness signals |
| dPZB5h5 | 0.4904 | 33m | $0.00 | success | Extract frames, measure shapes with PIL/numpy, implement superellipse morph in Revideo |
| p2VhvmH | 0.3386 | 24m | $0.00 | below_threshold | Polar formula morphing with per-row cosine-eased keyframes |

#### gpt-5.4

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| 4J8289j | 0.0 | 11m | $0.00 | anti_cheat_penalty | Extract frames, analyze pixels, build keyframed parametric shape morph |
| brjwmBm | 0.0 | 16m | $0.00 | anti_cheat_penalty | Extract contour radii from reference frames, embed as template arrays, interpolate between shape states |
| iiWRe5a | 0.2995 | 13m | $0.00 | below_threshold | Analyze reference with OpenCV, build parametric SVG path morphing in Revideo |

### Post-Rollout QA

| Check | Result |
|-------|--------|
| Trial verdicts | 6/6 FAIR |

<!-- END:ROLLOUT_RESULTS -->
