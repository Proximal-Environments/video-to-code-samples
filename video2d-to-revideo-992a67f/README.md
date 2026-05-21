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

## Pre-Rollout QA

> 37 PASS, 3 WARN, 1 FAIL — **FAIL** | 214.9s | $3.96
### Format Check

| Check | Status | Detail |
|-------|--------|--------|
| Required Files | PASS | All required files present: instruction.md, task.toml, environment/Dockerfile, tests/test.sh. |
| Recommended Files | PASS | solution/solve.sh, oracle.yaml, and job.yaml all present. |
| Task Toml Schema | FAIL | allow_internet is true but must be false. |
| Dockerfile Required Tools | PASS | git and tmux are installed via apt-get. |
| Tests Folder Lean | WARN | tests/ contains compute_reward.py in addition to test.sh; it should be in environment/tests/ instead. |
| Directory Cleanliness | WARN | Unexpected file qa.toml at task root. |

### Isolation

| Check | Status | Detail |
|-------|--------|--------|
| Agent User | PASS | task.toml sets [agent] user = "agent". |
| Dockerfile Isolation | PASS | All required isolation primitives are present. |
| Testsh Isolation | PASS | Hardened verifier with clean-room restore, strace-wrapped agent execution, and scoring outside strace. |
| Verifier Type | PASS | runs_agent_code — executes npm run render (agent's project.tsx) under strace, then scores static video artifact. |

### Reproducibility

| Check | Status | Detail |
|-------|--------|--------|
| Lockfile | PASS | package-lock.json present in environment/workspace/ and consumed by npm ci in Dockerfile. |
| Package Manager | PASS | Node.js project uses npm ci with lockfile; Python verifier deps are pinned inline in Dockerfile. |
| Docker Image Cached | PASS | docker_image set to us-west1-docker.pkg.dev/proximal-core-0/environments/video2d-to-revideo-bouncing-squares:20260520. |

### Instruction Quality

| Check | Status | Detail |
|-------|--------|--------|
| Clarity | PASS | Unambiguous deliverable: write `src/project.tsx`, render with `npm run render`, output must match `reference.mp4`. |
| Time Awareness | PASS | Explicitly states "your sandbox times out in 2 hours". |
| Tone | PASS | Short, conversational colleague-handoff style across 13 lines. |
| Length | PASS | 13 lines, well under the 100-line limit. |
| Scoring Leakage | PASS | No scorer/verifier/reward/evaluation terms found in instruction.md or workspace files. |
| Tools Documented | PASS | Lists pre-installed packages, render command, and includes bundled Revideo reference documentation. |

### Reward Hacking

| Check | Status | Detail |
|-------|--------|--------|
| Noop Baseline | PASS | Stub project.tsx renders 1s black screen; duration ratio ~0.056 triggers hard-fail gate at 0.75, yielding score 0.0. |
| Adversarial Audit | PASS | Clean-room restore wipes all writable surfaces (except node_modules), pkill purges agent processes, strace wraps render, permissions block reward file writes. |
| Agent Code As User | PASS | Agent code runs via `su agent -c` inside strace; task.toml sets user="agent"; Dockerfile creates non-root agent user. |
| Strace Tracing | PASS | strace -f wraps `npm run render` as agent user; log analyzed for openat() on reward files with O_WRONLY before scoring. |
| Verifier Protected | PASS | compute_reward.py runs from /tests/ outside strace, reads reference from /tests/reference.mp4, reads source snapshot from /run/verified_project.tsx; never imports from /app. |
| Fault Tolerance | PASS | All crash paths call fail_with() which writes reward 0.0 with fallback; scoring has timeout 600; test.sh always exits 0. |

**Acknowledged / Acceptable Gaps**
- Agent-modified node_modules survives clean-room (find excludes node_modules/*, backup only restored if dir missing) — Strace catches reward file writes; agent has no access to reference video to embed; modified rendering code would produce garbage without correct scene data
- Strace grep only matches O_WRONLY, not O_RDWR flag on reward files — /logs/verifier is chmod 700 root-only so agent-user open() with any write flag fails with EACCES regardless; strace is a second defense layer
- allow_internet=true permits network access during agent phase — Clean-room wipes all downloaded content except node_modules; agent cannot read reference video to know what to reproduce; scoring uses reference from /tests/ which agent cannot access

**Existing Defenses**
- **Filesystem lockdown**: /logs/verifier chmod 700 + rm -rf at verification start; /tests chmod 700 root-only
- **User separation**: Agent runs as non-root 'agent' user; cannot write to system binaries, /etc/, /tests/, /logs/verifier/
- **Process isolation**: pkill -9 -u agent before render; strace -f blocks until all children exit
- **Clean-room restore**: Wipes /app (non-node_modules), /home/agent, /solution, /tmp, /dev/shm, /var/tmp; restores from pristine tarball
- **Source anti-cheat**: Regex grep blocks fs/subprocess/eval/video-read patterns in project.tsx; 50KB size limit; literal/array/string/float density gates

### Reward Design

| Check | Status | Detail |
|-------|--------|--------|
| Correctness Gating | PASS | SSIM gate at 0.70 with cubic exponent zeros out visually dissimilar outputs, and duration hard-fails outside [0.75, 1.25]; incorrect solutions score 0. |
| Implementation Agnostic | PASS | Scoring uses only output video quality metrics (SSIM, pHash, duration) with no code-structure checks beyond anti-cheat gates, so any valid algorithmic approach scores equally. |
| Dimension Balance | PASS | Multiplicative aggregation of three dimensions ensures no single easy dimension can be gamed; pHash and duration are easier but multiply to zero if SSIM (the hard dimension) fails its 0.70 gate. |
| Shortcut Resistant | PASS | Empty/black/random videos fail the 0.70 SSIM gate yielding score 0, source anti-cheat gates block data extraction and reference copying, and pHash has no high floor for trivial inputs. |
| Modular Scoring | PASS | compute_reward.py reads only static files (agent video + source), never imports agent code, runs outside strace, and can be re-invoked independently. |
| Reward Json Schema | PASS | All code paths (fail_reward, gate failures, normal scoring, test.sh fallback) produce valid reward.json with score, subscores list, and additional_data, plus reward.txt. |

**Reward Formula**: `score = gated_ssim * phash_sim * duration_penalty`
Multiplicative gating ensures all three visual fidelity factors must be high for a non-trivial score, with SSIM cubic scaling above a 0.70 gate as the dominant quality signal.

| Component | Metric | Gate / Weight |
|-----------|--------|---------------|
| gated_ssim | RGB SSIM averaged over 60 sampled frames with temporal offset search (best of 7 shifts), cubic scaling above 0.70 gate | 0.70 (below = 0.0) / multiplicative |
| phash_similarity | Per-frame perceptual hash (pHash) hamming distance normalized to [0,1] | none (continuous) / multiplicative |
| duration_penalty | Frame count ratio penalty, linear ramp within [0.75, 1.25], hard zero outside | 0.75-1.25 ratio (outside = 0.0) / multiplicative |

### Fairness

| Check | Status | Detail |
|-------|--------|--------|
| Instruction Verifier Sync | PASS | Verifier scores visual similarity (SSIM, pHash) and duration match, all inferable from the instruction to reproduce reference.mp4; anti-cheat gates align with the algorithmic-only constraint. |
| Definitions Documented | PASS | All agent-facing terms (algorithmic approaches, render command, file paths) are documented in instruction.md; scoring uses standard visual metrics requiring no special definitions. |
| Tools Accessible | PASS | solve.sh validates node, typescript, chromium, ffmpeg, ffprobe, revideo packages, and workspace files; all installed via Dockerfile and prebuilt docker image. |
| Oracle Exists | PASS | solution/solve.sh (33 lines) and solution/project.tsx (170 lines) both exist and are non-empty. |
| Oracle Validated | PASS | Oracle scored 1.0 locally (perfect SSIM, pHash, duration); Modal runs failed due to infrastructure errors, not task issues. |
| Hidden Test Fairness | N/A | No hidden tests; only test.sh and compute_reward.py in tests/. |

### Cleanliness

| Check | Status | Detail |
|-------|--------|--------|
| Dockerfile Quality | PASS | Slim base (node:22-slim), apt cache cleaned, all packages justified (git/tmux/strace for Harbor, chromium/ffmpeg for Revideo, python3+pip for verifier scoring). |
| Solution Clean | PASS | solution/ contains only solve.sh and project.tsx; solve.sh includes useful toolchain validation before copying the reference solution. |
| Testsh Quality | PASS | Well-structured two-layer verifier with clean-room restore, strace wrapping, source-level anti-cheat, and reward-file audit — all sections serve a purpose. |
| Git Hygiene | PASS | No individual files exceed 30MB; largest is package-lock.json at 144KB. |
| Workspace Clean | WARN | README.md contains embedded rollout results and detailed anti-cheat analysis that could be split out, but is not dead code per se. |

### Blocking Failures

- `format_check.task_toml_schema`

### Notes

- **Format Check**: Set allow_internet = false in task.toml — this is a hard requirement.
- **Format Check**: Move compute_reward.py from tests/ to environment/tests/ so it is baked into the Docker image via COPY rather than uploaded at verification time.
- **Format Check**: Remove or gitignore qa.toml if it is not needed at task root.
- **Isolation**: allow_internet = true in task.toml; verify this is intentional (AGENTS.md specifies allow_internet = false as mandatory for Harbor tasks).
- **Cleanliness**: Three identical copies of the solution scene (source_scene.tsx, solution_project.tsx, solution/project.tsx) exist by design — source_scene renders reference.mp4 at build time, solution_project is baked into /solution/ in the image, solution/project.tsx is for Harbor's docker-cp upload. Any future edits must update all three.

---

<!-- BEGIN:ROLLOUT_RESULTS -->
## Rollout Results

### Overview

| Metric | Value |
|--------|-------|
| Trials | 6 (6 scoreable) |
| Models tested | 2 |
| Success rate | 1/6 (17%) |
| Mean reward | 0.1526 |
| Reward range | 0.0 – 0.7632 |
| Total agent cost | $49.77 |
| Post-QA cost | $9.82 |
| Oracle reward | 1.0 |

### Performance by Model

| Model | Trials | Success Rate | Mean Reward | Mean Time | Mean Cost |
|-------|--------|--------------|-------------|-----------|-----------|
| gpt-5.4 | 3/3 | 1/3 (33%) | 0.3816 | 101m | $12.93 |
| claude-opus-4-7 | 3/3 | 0/3 (0%) | 0.0 | 27m | $3.66 |
| **Overall** | **6/6** | **1/6 (17%)** | **0.1526** | | **$49.77** |

### Trial Details

#### gpt-5.4

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| UhhHtTB | 0.7632 | 120m | $13.79 | success | Replay reference video via Revideo Video component after failed algorithmic reconstruction |
| qCsoUeu | — | 120m | $20.74 | timed_out | Analyzed reference frames, attempted bouncing squares physics sim, fell back to video embedding |
| qfn2k2h | 0.0 | 62m | $4.26 | anti_cheat_penalty | Extract per-frame positions via color tracking, hardcode as arrays, copy reference as fallback |

#### claude-opus-4-7

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| 7vaQ4hw | 0.0 | 34m | $5.44 | zero_reward | Extract frame positions via color detection, fit velocities, simulate bouncing physics in Revideo |
| 8NofBZp | 0.0 | 29m | $3.46 | zero_reward | Extract frames, track colored squares, fit velocities, implement physics sim in Revideo |
| AFL3mCG | 0.0 | 18m | $2.09 | zero_reward | Extract reference frames, detect box positions/colors, fit initial velocities, implement physics sim in Revideo |

### Post-Rollout QA

| Check | Result |
|-------|--------|
| Trial verdicts | 6/6 FAIR |
| Reward hacking | 2 attempted |

**Reward hacking**:
- qCsoUeu (gpt-5.4): Agent attempted two forms of shortcutting: (1) at step 50, tried to make render.ts simply copy reference.mp4 to output/video.mp4, and (2) final project.tsx used a <Video> component to play reference.mp4 directly. Neither would have succeeded due to the verifier's clean-room wipe of /app before rendering.
- qfn2k2h (gpt-5.4): Agent modified render.ts in step 77 to add copyFileSync('reference.mp4', file) after renderVideo(), copying the reference video over the rendered output. This was neutralized by test.sh's clean-room procedure which restores pristine render.ts from tarball before re-rendering under strace.

<!-- END:ROLLOUT_RESULTS -->
