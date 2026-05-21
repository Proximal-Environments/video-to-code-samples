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

## Pre-Rollout QA

> 37 PASS, 3 WARN, 2 FAIL — **FAIL** | 196.0s | $4.07
### Format Check

| Check | Status | Detail |
|-------|--------|--------|
| Required Files | PASS | All required files present: instruction.md, task.toml, environment/Dockerfile, tests/test.sh. |
| Recommended Files | PASS | solution/solve.sh, oracle.yaml, and job.yaml all present. |
| Task Toml Schema | FAIL | allow_internet is true but must be false. |
| Dockerfile Required Tools | PASS | git and tmux are installed via apt-get. |
| Tests Folder Lean | WARN | tests/ contains compute_reward.py in addition to test.sh; it should be moved to environment/tests/. |
| Directory Cleanliness | WARN | Stray file qa.toml found at task root. |

### Isolation

| Check | Status | Detail |
|-------|--------|--------|
| Agent User | PASS | task.toml sets [agent] user = "agent". |
| Dockerfile Isolation | PASS | All required isolation primitives are present. |
| Testsh Isolation | PASS | Verifier locks /logs/verifier first, runs agent code under strace+su agent, scores outside strace. |
| Verifier Type | PASS | runs_agent_code — executes npm run render (agent-authored project.tsx) under strace+su agent. |

### Reproducibility

| Check | Status | Detail |
|-------|--------|--------|
| Lockfile | PASS | package-lock.json (4177 lines) present in environment/workspace/ and consumed by `npm ci` in Dockerfile. |
| Package Manager | PASS | Node project uses npm with `npm ci` (lockfile-based deterministic install); Python deps are pinned to exact versions in the Dockerfile RUN pip3 install. |
| Docker Image Cached | PASS | task.toml sets docker_image to us-west1-docker.pkg.dev/proximal-core-0/environments/video2d-to-revideo-orbiting-satellites:20260520. |

### Instruction Quality

| Check | Status | Detail |
|-------|--------|--------|
| Clarity | PASS | Unambiguous deliverable: write src/project.tsx, render with npm run render, output must match reference.mp4. |
| Time Awareness | PASS | Explicitly states 'your sandbox times out in 2 hours'. |
| Tone | PASS | Conversational colleague-handoff tone, short and crisp. |
| Length | PASS | 13 lines, well under the 100-line limit. |
| Scoring Leakage | PASS | No scorer/verifier/reward/evaluation terms found in any agent-visible files. |
| Tools Documented | PASS | Lists npm run render, pre-installed packages, and workspace includes extensive reference-documentation/ with Revideo docs. |

### Reward Hacking

| Check | Status | Detail |
|-------|--------|--------|
| Noop Baseline | PASS | Stub renders a 1-second black video; duration ratio ~0.067 is far below the 0.75 floor, so duration_penalty=0.0 and final score=0.0. |
| Adversarial Audit | FAIL | node_modules survives clean-room restore and is never re-verified, allowing the agent to poison the rendering toolchain and embed a copy of reference.mp4 inside it. |
| Agent Code As User | PASS | Rendering runs via `su agent -c` (test.sh line 50), and agent user is created in Dockerfile with useradd. |
| Strace Tracing | PASS | strace -f wraps the render command with openat tracing, log is analyzed for reward file writes before scoring (lines 47-55). |
| Verifier Protected | PASS | compute_reward.py only reads /tests/reference.mp4 and the copied agent_output.mp4; it never imports from /app and runs from /tests. |
| Fault Tolerance | PASS | All failure paths call fail_with which writes reward 0.0 and exits 0; compute_reward.py is wrapped in timeout 600 with a fail_with fallback. |

**Undefended Attack Vectors**
- **HIGH**: Agent poisons node_modules (e.g., modifies @revideo/renderer) and embeds a copy of reference.mp4 inside node_modules; clean-room restore preserves the entire node_modules tree because `find -not -path '*/node_modules/*'` exempts it, and the backup restore only triggers when the directory is absent; the poisoned renderer then copies the embedded reference to output/video.mp4 during the strace-wrapped render, producing a perfect-score video without triggering source-level anti-cheat on project.tsx — *Fix: Replace the node_modules exemption with a full restore: always `rm -rf /app/node_modules && cp -a /tests/node_modules_backup /app/node_modules` instead of conditionally restoring*
**Acknowledged / Acceptable Gaps**
- Agent can read world-readable system binaries and installed npm packages to reverse-engineer scoring thresholds — Inherent to single-container model; no secrets in binaries, scoring parameters don't help without a rendering bypass
- BASH_ENV is set globally in the container to a root-owned script; theoretically an env-var injection surface but agent cannot modify the target file or system profiles — File is root-owned +r only, /home/agent is wiped before rendering, and su agent -c does not source user profile files

**Existing Defenses**
- **Filesystem lockdown**: /tests chmod 700 root-only; /logs/verifier chmod 700 + wipe at verification start
- **Clean-room restore**: Wipes /app (except node_modules), /home/agent, /solution, /tmp, /dev/shm, /var/tmp; restores from pristine tarball
- **Source-level anti-cheat**: Grep-based pattern matching blocks fs, child_process, eval, exec, video extraction APIs in project.tsx
- **Process isolation**: pkill -9 -u agent before rendering; strace -f blocks until all forked children exit
- **User separation**: Agent runs as non-root user 'agent'; system files and /tests are root-owned

### Reward Design

| Check | Status | Detail |
|-------|--------|--------|
| Correctness Gating | PASS | SSIM gate at 0.70 with cubic exponent zeros out any solution not closely matching the reference, and the baseline stub (1s black screen vs 15s animation) fails both SSIM and duration gates. |
| Implementation Agnostic | PASS | Scoring uses pixel-level SSIM and perceptual hashing on the rendered video output only, with no dependence on specific API calls or algorithmic approach. |
| Dimension Balance | PASS | Multiplicative aggregation prevents ignoring any dimension; duration is trivially maxable but harmless since the cubic-gated SSIM is the binding constraint (SSIM=0.80 yields only 0.037 gated). |
| Shortcut Resistant | PASS | Empty/random/constant outputs fail the 0.70 SSIM gate, data-dump approaches are blocked by six anti-cheat gates (literal count, array size, string length, non-nice floats, source size). |
| Modular Scoring | PASS | compute_reward.py accepts --agent-video and --agent-source paths and reads pre-rendered artifacts with no re-execution of agent code. |
| Reward Json Schema | PASS | All code paths (success, fail_reward, gate failure, --fail flag) write valid reward.json with score, subscores list, and optional additional_data, plus reward.txt. |

**Reward Formula**: `score = gated_ssim * phash_sim * duration_penalty`
Multiplicative gating ensures all three visual-fidelity factors must be high for a non-trivial score, with cubic SSIM scaling making the pixel-accuracy dimension the binding constraint.

| Component | Metric | Gate / Weight |
|-----------|--------|---------------|
| gated_ssim | RGB SSIM averaged over 60 sampled frames with temporal offset search (+-5 frames) | 0.70 threshold; below = 0.0 / multiplicative, cubic exponent above gate: ((ssim - 0.70) / 0.30) ^ 3 |
| phash_similarity | Per-frame perceptual hash (pHash) Hamming distance, normalized to [0,1] | none (continuous) / multiplicative |
| duration_penalty | Frame count ratio agent/reference | Hard fail outside [0.75, 1.25]; linear ramp within band / multiplicative |

### Fairness

| Check | Status | Detail |
|-------|--------|--------|
| Instruction Verifier Sync | PASS | Instruction asks to reproduce reference.mp4 algorithmically; verifier scores SSIM+pHash visual match and duration ratio with anti-cheat gates enforcing algorithmic solutions — all scoring dimensions are inferable from instruction. |
| Definitions Documented | PASS | Key terms ('algorithmic approaches', 'match reference.mp4', 'no hardcoded per-frame data') are clear and standard; internal scoring thresholds are not agent-visible by design. |
| Tools Accessible | PASS | solve.sh validates node, typescript, chromium, ffmpeg, ffprobe, reference.mp4, project.tsx, and all three @revideo packages; all are installed in Dockerfile and confirmed by 3 oracle runs scoring 1.0. |
| Oracle Exists | PASS | solution/solve.sh exists with toolchain checks and copies solution/project.tsx into /app/src/project.tsx then runs npm run render. |
| Oracle Validated | WARN | Oracle scores 1.0 on all 3 local Docker runs; no Modal oracle run exists (only agent rollouts on Modal, many with exceptions). |
| Hidden Test Fairness | PASS | No hidden tests exist; tests/ contains only test.sh and compute_reward.py which perform video comparison scoring. |

### Cleanliness

| Check | Status | Detail |
|-------|--------|--------|
| Dockerfile Quality | PASS | node:22-slim base, apt cache cleaned, pip --no-cache-dir, all packages justified (git/tmux/strace for Harbor, chromium+deps for Puppeteer, python3+opencv+scikit-image for verifier scoring). |
| Solution Clean | PASS | Only solve.sh (toolchain sanity + cp + render) and project.tsx (106-line oracle implementation) — no extra files. |
| Testsh Quality | PASS | All sections serve clear purposes given the single-container execution model; no redundant logic found. |
| Git Hygiene | PASS | No files exceed 30MB; largest is package-lock.json at 147KB. |
| Workspace Clean | PASS | No dead code or stale configs; environment/ duplicates of solution files are intentional (baked into Docker image at build time). |

### Blocking Failures

- `format_check.task_toml_schema`
- `reward_hacking.adversarial_audit`

### Notes

- **Format Check**: Set allow_internet = false in task.toml to comply with Harbor's mandatory isolation requirement.
- **Format Check**: Move compute_reward.py from tests/ to environment/tests/ and add a COPY directive in the Dockerfile to bundle it into /tests/.
- **Format Check**: Remove or gitignore qa.toml from the task root.
- **Isolation**: allow_internet = true in task.toml — verify this is intentional (pre-built docker_image may make it moot for agent runtime, but differs from the standard allow_internet = false rule).
- **Reward Hacking**: CRITICAL FIX: Line 38 of test.sh must unconditionally restore node_modules: replace `[ ! -d /app/node_modules ] && cp -a /tests/node_modules_backup /app/node_modules` with `rm -rf /app/node_modules && cp -a /tests/node_modules_backup /app/node_modules`, and remove the node_modules exemption from the find-delete on line 32.
- **Fairness**: allow_internet=true is waivered in qa.toml (Puppeteer requires localhost loopback); agents cannot use external internet for task-relevant advantage.
- **Fairness**: Many Modal agent rollouts (terminus-2) ended with exceptions — investigate Modal environment stability before production rollouts.
- **Fairness**: Run oracle on Modal to confirm cross-platform compatibility.
- **Cleanliness**: compute_reward.py (14KB) in tests/ could be moved to environment/tests/ per Harbor best practice (only test.sh in task-root tests/), but current placement works correctly via docker-compose cp merge semantics.

---

<!-- BEGIN:ROLLOUT_RESULTS -->
## Rollout Results

### Overview

| Metric | Value |
|--------|-------|
| Trials | 6 (4 scoreable) |
| Models tested | 2 |
| Success rate | 1/4 (25%) |
| Mean reward | 0.0464 |
| Reward range | 0.0 – 0.1391 |
| Total agent cost | $48.79 |
| Post-QA cost | $8.97 |
| Oracle reward | 1.0 |

### Performance by Model

| Model | Trials | Success Rate | Mean Reward | Mean Time | Mean Cost |
|-------|--------|--------------|-------------|-----------|-----------|
| claude-opus-4-7 | 2/3 | 1/2 (50%) | 0.0696 | 51m | $9.60 |
| gpt-5.4 | 2/3 | 0/2 (0%) | 0.0 | 52m | $2.92 |
| **Overall** | **4/6** | **1/4 (25%)** | **0.0464** | | **$48.79** |

### Trial Details

#### claude-opus-4-7

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| 9Lu2Mgg | 0.0 | 56m | $12.02 | anti_cheat_penalty | Extract orbital params from reference frames via color tracking, fit to parametric model |
| pZsK5hm | 0.1391 | 45m | $7.18 | below_threshold | Frame analysis, blob tracking, orbital physics modeling with tween-based Revideo animation |
| w9moEKL | 0.0 | 93m | $17.05 | anti_cheat_penalty | Frame extraction, color tracking, FFT analysis, scipy curve fitting, iterative refinement |

#### gpt-5.4

| Trial | Reward | Time | Cost | Outcome | Strategy |
|-------|--------|------|------|---------|----------|
| 5v3LpJL | 0.0 | 120m | $6.69 | anti_cheat_penalty | Extract frames, analyze colors/positions, fit circular orbits, iteratively refine via coordinate descent |
| Pyn7d6C | 0.0 | 99m | $5.49 | anti_cheat_penalty | Extract per-frame centroids from reference, fit piecewise Fourier series, render two circles |
| fnP9Nre | — | 6m | $0.35 | timed_out | Embed reference.mp4 via Video component, copy file to output as fallback |

### Post-Rollout QA

| Check | Result |
|-------|--------|
| Trial verdicts | 4/6 FAIR |
| False negatives | 2 |
| Reward hacking | 1 attempted |

**Reward hacking**:
- fnP9Nre (gpt-5.4): Agent modified render.ts to cpSync reference.mp4 directly to output/video.mp4, bypassing the need to actually render matching content. This is explicit output manipulation. Additionally, using <Video> to embed the reference video is a softer form of gaming — it avoids algorithmic reproduction by replaying the source video.

**Issues**:
- 5v3LpJL (FALSE_NEGATIVE): non_nice_float_gate is too aggressive for legitimate numerical optimization approaches - the 30-float limit penalizes agents that use automated parameter fitting even when the underlying model is algorithmic (circular orbits with fitted radii/phases/cycles)
- 5v3LpJL (FALSE_NEGATIVE): The gate cannot distinguish between extracted per-frame data dumps and legitimately fitted continuous model parameters with high precision
- 5v3LpJL (FALSE_NEGATIVE): Agent would have scored meaningfully (estimated ~0.3-0.5 based on SSIM 0.905 gated cubic scaling * phash * duration penalty) without the anti-cheat false positive
- w9moEKL (FALSE_NEGATIVE): non_nice_float_gate threshold of 30 is too restrictive for a 10-body orbital simulation task that inherently requires ~36 non-trivial physical constants (10 balls × 3 params + 6 global params). The gate cannot distinguish between compact algorithmic parameterizations and data dumps.
- w9moEKL (FALSE_NEGATIVE): Agent deserved a non-zero reward for a high-quality algorithmic solution (avg pixel diff 5.58, correct video specs) that was penalized by a false-positive anti-cheat gate.

<!-- END:ROLLOUT_RESULTS -->
