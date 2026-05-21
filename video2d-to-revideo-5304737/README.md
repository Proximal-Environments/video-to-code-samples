# Orbiting Satellites Revideo Animation

> Reproduce a reference animation of 6 satellites orbiting a central circle through 3 orbital phases with changing radii and direction. Agent writes a Revideo scene in TypeScript that renders to a matching video.

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
| Success rate | 3/6 (50%) |
| Mean reward | 0.0597 |
| Reward range | 0.0 – 0.1809 |
| Total agent cost | $0.00 |
| Post-QA cost | $9.54 |
| Oracle reward | 1.0 |

### Performance by Model

| Model | Trials | Success Rate | Mean Reward | Mean Time | Mean Cost |
|-------|--------|--------------|-------------|-----------|-----------|
| claude-opus-4-7 | 3/3 | 2/3 (67%) | 0.0955 | 12m | $0.00 |
| gpt-5.4 | 3/3 | 1/3 (33%) | 0.006 | 19m | $0.00 |
| **Overall** | **6/6** | **3/6 (50%)** | **0.0597** | | **$0.00** |

### Trial Details

#### claude-opus-4-7

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| BzbaAgk | 0.1809 | 16m | $0.00 | below_threshold | Frame extraction, color/position tracking, orbital parameter fitting, Revideo parametric animation |
| T74bmif | 0.1056 | 14m | $0.00 | below_threshold | Extract reference frames, detect circles by color, fit orbital parameters, render Revideo scene |
| nuaRiy4 | 0.0 | 5m | $0.00 | anti_cheat_penalty | Visual frame analysis then Lissajous parametric motion model with hand-tuned constants |

#### gpt-5.4

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| ADJUff2 | 0.0119 | 14m | $0.00 | below_threshold | CV2 Hough circle detection + frequency fitting to derive orbital model for Revideo scene |
| VSZ5FHU | 0.0 | 30m | $0.00 | anti_cheat_penalty | Extract frame positions via CV, fit DCT curves, encode as coefficients in Revideo |
| ppGVG7f | — | 12m | $0.00 | timed_out | Attempted algorithmic orbital reconstruction, timed out before rendering |

### Post-Rollout QA

| Check | Result |
|-------|--------|
| Trial verdicts | 6/6 FAIR |

<!-- END:ROLLOUT_RESULTS -->
