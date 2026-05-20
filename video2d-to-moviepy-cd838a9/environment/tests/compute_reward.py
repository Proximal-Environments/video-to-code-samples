#!/usr/bin/env python3
"""Video-to-Code scorer.

  score = gated_ssim * phash_sim * duration_penalty

Multiplicative gating — all three factors must be high for a non-trivial score.

Factors:
  gated_ssim       -- RGB SSIM averaged over 60 sampled frames, with temporal
                      offset search (try +/-5 frame shifts, pick best alignment).
                      Gate at 0.70, cubic scaling above the gate.
  phash_sim        -- Per-frame perceptual hash (pHash) similarity. Catches
                      structural/layout differences that SSIM might average out.
                      Hamming distance normalized to [0, 1].
  duration_penalty -- Continuous penalty for frame count mismatch.
                      Hard fail outside [0.75x, 1.25x]. Linear ramp within.

Anti-cheat gates (per-task thresholds baked at Docker build time):
  source_size_gate     -- 5x oracle solution byte count.
  dump_literal_gate    -- Total numeric literals > MARGIN * oracle count.
  flat_array_gate      -- Largest bracketed numeric array > MARGIN * oracle max.
  string_lit_gate      -- Longest single-line string literal > MARGIN * oracle max
                          (excludes triple-quoted docstrings).
  total_str_gate       -- Sum of single-line string literal chars > MARGIN * oracle total.
  non_nice_float_gate  -- Count of non-0.25-multiple float literals > 30. Catches
                          extracted/fitted data with arbitrary decimals.

Temporal alignment:
  Tries offsets [-5, -3, -1, 0, +1, +3, +5] frames to find best SSIM
  alignment. Handles agents whose animation is correct but starts
  slightly early/late relative to the reference.
"""
from __future__ import annotations

import argparse
import json
import os
import re

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

N_SAMPLE_FRAMES = 60
SSIM_GATE = 0.70
SSIM_EXPONENT = 3
TEMPORAL_OFFSETS = [-5, -3, -1, 0, 1, 3, 5]
DURATION_RATIO_MIN = 0.75
DURATION_RATIO_MAX = 1.25

MAX_SOURCE_BYTES = 50_000
SOURCE_SIZE_MULTIPLIER = 5

DUMP_LITERAL_MARGIN = 5
DUMP_LITERAL_FLOOR = 580
FLAT_ARRAY_MARGIN = 5
FLAT_ARRAY_FLOOR = 150
STRING_LIT_MARGIN = 5
STRING_LIT_FLOOR = 335
TOTAL_STR_MARGIN = 5
TOTAL_STR_FLOOR = 1220
NON_NICE_FLOAT_LIMIT = 30

_LITERAL_RE = re.compile(r"-?\d+\.?\d*")
_COMMENT_RE = re.compile(r"#.*$", re.MULTILINE)
_STRING_RE = re.compile(
    r'"""(.*?)"""|'
    r"'''(.*?)'''|"
    r'"((?:[^"\\]|\\.)*)"|'
    r"'((?:[^'\\]|\\.)*)'",
    re.DOTALL,
)
# Excludes triple-quoted strings (docstrings) — only single-line
# string literals can carry encoded data payloads.
_DATA_STRING_RE = re.compile(
    r'"((?:[^"\\\n]|\\.)*)"|'
    r"'((?:[^'\\\n]|\\.)*)'",
)


# -- text analysis helpers (shared with precompute_ref.py) --------------------

def count_literals(text: str) -> int:
    return len(_LITERAL_RE.findall(text))


def strip_comments(text: str) -> str:
    return _COMMENT_RE.sub("", text)


def max_string_literal_length(text: str) -> int:
    """Longest single-line string literal (excludes triple-quoted docstrings)."""
    code = strip_comments(text)
    return max(
        (len(m.group(1) or m.group(2) or "")
         for m in _DATA_STRING_RE.finditer(code)),
        default=0,
    )


def total_string_literal_length(text: str) -> int:
    """Sum of chars across single-line string literals (excludes docstrings)."""
    code = strip_comments(text)
    return sum(
        len(m.group(1) or m.group(2) or "")
        for m in _DATA_STRING_RE.finditer(code)
    )


def max_flat_array_size(text: str) -> int:
    """Largest count of numeric literals in any single top-level bracketed expression."""
    depth, starts, max_count = 0, [], 0
    for i, c in enumerate(text):
        if c == "[":
            if depth == 0:
                starts.append(i)
            depth += 1
        elif c == "]":
            depth = max(0, depth - 1)
            if depth == 0 and starts:
                start = starts.pop()
                n = len(_LITERAL_RE.findall(text[start + 1 : i]))
                if n > max_count:
                    max_count = n
    return max_count


# -- I/O helpers --------------------------------------------------------------

def write_reward(outdir: str, score: float, subscores: list,
                 additional_data: dict | None = None) -> None:
    result = {"score": round(score, 6), "subscores": subscores}
    if additional_data:
        result["additional_data"] = additional_data
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "reward.json"), "w") as f:
        json.dump(result, f, indent=2)
    with open(os.path.join(outdir, "reward.txt"), "w") as f:
        f.write(f"{score}\n")
    print(f"\nReward: {score}")


def fail_reward(outdir: str, reason: str) -> None:
    write_reward(outdir, 0.0, [], {"reason": reason})


# -- anti-cheat gates ---------------------------------------------------------

def _load_thresholds() -> dict:
    """Load per-task thresholds baked at Docker build time."""
    path = "/tests/gate_thresholds.json"
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def check_source_size(source_path: str, thresholds: dict) -> tuple[bool, dict]:
    if not os.path.exists(source_path):
        return False, {"error": "source_not_found"}
    size = os.path.getsize(source_path)
    limit = thresholds.get("source_size_limit", MAX_SOURCE_BYTES)
    passed = size <= limit
    return passed, {"source_bytes": size, "limit": limit}


def check_dump_gate(source_path: str, thresholds: dict) -> tuple[bool, dict]:
    threshold = thresholds.get("dump_threshold", DUMP_LITERAL_FLOOR)
    oracle_lits = thresholds.get("source_literals", 0)
    info = {"threshold": threshold, "source_literals": oracle_lits}
    if not os.path.exists(source_path):
        info["agent_literals"] = -1
        return True, info
    with open(source_path) as f:
        count = count_literals(f.read())
    info["agent_literals"] = count
    triggered = count > threshold
    info["triggered"] = triggered
    return not triggered, info


def check_flat_array_gate(source_path: str, thresholds: dict) -> tuple[bool, dict]:
    threshold = thresholds.get("flat_array_threshold", FLAT_ARRAY_FLOOR)
    oracle_max = thresholds.get("source_max_array", 0)
    info = {"threshold": threshold, "source_max_array": oracle_max}
    if not os.path.exists(source_path):
        info["agent_max_array"] = -1
        return True, info
    with open(source_path) as f:
        max_arr = max_flat_array_size(f.read())
    info["agent_max_array"] = max_arr
    triggered = max_arr > threshold
    info["triggered"] = triggered
    return not triggered, info


def check_string_lit_gate(source_path: str, thresholds: dict) -> tuple[bool, dict]:
    threshold = thresholds.get("string_lit_threshold", STRING_LIT_FLOOR)
    oracle_max = thresholds.get("oracle_max_string", 0)
    info = {"threshold": threshold, "oracle_max_string": oracle_max}
    if not os.path.exists(source_path):
        info["agent_max_string"] = -1
        return True, info
    with open(source_path) as f:
        agent_max = max_string_literal_length(f.read())
    info["agent_max_string"] = agent_max
    triggered = agent_max > threshold
    info["triggered"] = triggered
    return not triggered, info


def check_total_str_gate(source_path: str, thresholds: dict) -> tuple[bool, dict]:
    threshold = thresholds.get("total_str_threshold", TOTAL_STR_FLOOR)
    oracle_total = thresholds.get("oracle_total_string", 0)
    info = {"threshold": threshold, "oracle_total_string": oracle_total}
    if not os.path.exists(source_path):
        info["agent_total_string"] = -1
        return True, info
    with open(source_path) as f:
        agent_total = total_string_literal_length(f.read())
    info["agent_total_string"] = agent_total
    triggered = agent_total > threshold
    info["triggered"] = triggered
    return not triggered, info


def check_non_nice_float_gate(source_path: str, thresholds: dict) -> tuple[bool, dict]:
    """Reject source with too many non-0.25-multiple float literals.
    Arbitrary decimals like 0.031321 or 29.175837 indicate extracted/fitted
    data from the reference video rather than algorithmic code."""
    limit = NON_NICE_FLOAT_LIMIT
    info = {"limit": limit}
    if not os.path.exists(source_path):
        info["agent_non_nice"] = -1
        return True, info
    with open(source_path) as f:
        text = f.read()
    _float_re = re.compile(r'(?<![a-zA-Z_])(\d+\.\d+)(?![a-zA-Z_])')
    easing_vals = {'7.5625', '2.75', '0.9375', '0.984375', '2.625', '0.075'}
    code = strip_comments(text)
    count = 0
    for line in code.split('\n'):
        if any(x in line for x in easing_vals):
            continue
        for m in _float_re.finditer(line):
            val = float(m.group(1))
            if val == 0.0 or abs(val - 0.01) < 0.001:
                continue
            r = val % 0.25
            if r > 0.001 and r < 0.249:
                count += 1
    info["agent_non_nice"] = count
    triggered = count > limit
    info["triggered"] = triggered
    return not triggered, info


# -- frame extraction ---------------------------------------------------------

def extract_frames_rgb(video_path: str,
                       n_frames: int = N_SAMPLE_FRAMES) -> list[np.ndarray]:
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total <= 0:
        cap.release()
        return []
    indices = np.linspace(0, total - 1, min(n_frames, total), dtype=int)
    frames: list[np.ndarray] = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames


# -- pHash similarity ---------------------------------------------------------

def _phash_frame(frame_rgb: np.ndarray) -> np.ndarray:
    """Compute 8x8 DCT-based perceptual hash (64-bit)."""
    gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
    resized = cv2.resize(gray, (32, 32), interpolation=cv2.INTER_AREA)
    dct = cv2.dct(np.float32(resized))
    dct_low = dct[:8, :8]
    med = np.median(dct_low)
    return (dct_low > med).flatten().astype(np.uint8)


def compute_phash_similarity(ref_frames: list[np.ndarray],
                             agent_frames: list[np.ndarray]) -> tuple[float, dict]:
    n = min(len(ref_frames), len(agent_frames))
    if n == 0:
        return 0.0, {"error": "no_frames"}

    distances = []
    for i in range(n):
        ref_f = ref_frames[i]
        agent_f = agent_frames[i]
        if ref_f.shape != agent_f.shape:
            agent_f = cv2.resize(agent_f, (ref_f.shape[1], ref_f.shape[0]))
        h1 = _phash_frame(ref_f)
        h2 = _phash_frame(agent_f)
        distances.append(int(np.sum(h1 != h2)))

    mean_dist = float(np.mean(distances))
    similarity = max(0.0, 1.0 - mean_dist / 32.0)
    return round(similarity, 4), {
        "mean_hamming": round(mean_dist, 2),
        "max_hamming": int(np.max(distances)),
        "frames_compared": n,
    }


# -- temporal alignment -------------------------------------------------------

def _quick_ssim(ref_frames: list[np.ndarray],
                agent_frames: list[np.ndarray],
                sample: int = 10) -> float:
    n = min(len(ref_frames), len(agent_frames))
    if n == 0:
        return 0.0
    step = max(1, n // sample)
    scores = []
    for i in range(0, n, step):
        ref_f = ref_frames[i]
        agent_f = agent_frames[i]
        if ref_f.shape != agent_f.shape:
            agent_f = cv2.resize(agent_f, (ref_f.shape[1], ref_f.shape[0]))
        scores.append(ssim(ref_f, agent_f, channel_axis=2))
    return float(np.mean(scores))


def find_best_offset(ref_frames: list[np.ndarray],
                     agent_frames: list[np.ndarray]) -> tuple[int, float]:
    best_ssim = -1.0
    best_offset = 0
    for offset in TEMPORAL_OFFSETS:
        if offset >= 0:
            r = ref_frames[offset:]
            a = agent_frames[:len(r)]
        else:
            a = agent_frames[-offset:]
            r = ref_frames[:len(a)]
        if not r or not a:
            continue
        s = _quick_ssim(r, a)
        if s > best_ssim:
            best_ssim = s
            best_offset = offset
    return best_offset, best_ssim


# -- gated RGB SSIM -----------------------------------------------------------

def compute_ssim_score(ref_frames: list[np.ndarray],
                       agent_frames: list[np.ndarray]) -> tuple[float, dict]:
    n = min(len(ref_frames), len(agent_frames))
    if n == 0:
        return 0.0, {"error": "no_frames"}

    scores = []
    for i in range(n):
        ref_f = ref_frames[i]
        agent_f = agent_frames[i]
        if ref_f.shape != agent_f.shape:
            agent_f = cv2.resize(agent_f, (ref_f.shape[1], ref_f.shape[0]))
        s = ssim(ref_f, agent_f, channel_axis=2)
        scores.append(s)

    mean_raw = float(np.mean(scores))
    info = {
        "mean_ssim": round(mean_raw, 4),
        "min_ssim": round(float(np.min(scores)), 4),
        "max_ssim": round(float(np.max(scores)), 4),
        "frames_compared": n,
        "gate": SSIM_GATE,
        "exponent": SSIM_EXPONENT,
    }

    if mean_raw < SSIM_GATE:
        info["gated"] = 0.0
        return 0.0, info

    gated = ((mean_raw - SSIM_GATE) / (1.0 - SSIM_GATE)) ** SSIM_EXPONENT
    info["gated"] = round(gated, 4)
    return round(gated, 4), info


# -- duration penalty ---------------------------------------------------------

def compute_duration_penalty(ref_count: int,
                             agent_count: int) -> tuple[float, dict]:
    if ref_count == 0:
        return 0.0, {"error": "no_ref_frames"}
    ratio = agent_count / ref_count
    info = {
        "ref_frames": ref_count,
        "agent_frames": agent_count,
        "ratio": round(ratio, 4),
    }
    if ratio < DURATION_RATIO_MIN or ratio > DURATION_RATIO_MAX:
        info["penalty"] = 0.0
        return 0.0, info
    if ratio <= 1.0:
        penalty = (ratio - DURATION_RATIO_MIN) / (1.0 - DURATION_RATIO_MIN)
    else:
        penalty = (DURATION_RATIO_MAX - ratio) / (DURATION_RATIO_MAX - 1.0)
    info["penalty"] = round(penalty, 4)
    return round(penalty, 4), info


# -- main ---------------------------------------------------------------------

GATE_CHECKS = [
    ("source_size_gate", check_source_size),
    ("dump_literal_gate", check_dump_gate),
    ("flat_array_gate", check_flat_array_gate),
    ("string_lit_gate", check_string_lit_gate),
    ("total_str_gate", check_total_str_gate),
    ("non_nice_float_gate", check_non_nice_float_gate),
]


def main():
    parser = argparse.ArgumentParser(description="Video-to-code scorer")
    parser.add_argument("--fail", help="Hard failure reason")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--agent-video", help="Path to agent-produced video")
    parser.add_argument("--agent-source", help="Path to agent source for size gate")
    args = parser.parse_args()

    if args.fail:
        fail_reward(args.output_dir, args.fail)
        return

    thresholds = _load_thresholds()

    if args.agent_source:
        for gate_name, gate_fn in GATE_CHECKS:
            passed, gate_info = gate_fn(args.agent_source, thresholds)
            if not passed:
                write_reward(args.output_dir, 0.0,
                    [{"subtask": gate_name, "score": 0.0}],
                    {"gate_failed": gate_name, "info": gate_info})
                return

    ref_path = "/tests/reference.mp4"
    if not os.path.exists(ref_path):
        fail_reward(args.output_dir, "no_reference_video")
        return

    agent_video = args.agent_video or "/app/output.mp4"
    if not os.path.exists(agent_video):
        fail_reward(args.output_dir, "no_agent_video")
        return

    ref_frames = extract_frames_rgb(ref_path)
    agent_frames = extract_frames_rgb(agent_video)
    if not ref_frames:
        fail_reward(args.output_dir, "ref_no_frames")
        return
    if not agent_frames:
        fail_reward(args.output_dir, "agent_no_frames")
        return

    offset, _ = find_best_offset(ref_frames, agent_frames)
    if offset >= 0:
        aligned_ref = ref_frames[offset:]
        aligned_agent = agent_frames[:len(aligned_ref)]
    else:
        aligned_agent = agent_frames[-offset:]
        aligned_ref = ref_frames[:len(aligned_agent)]

    ssim_score, ssim_info = compute_ssim_score(aligned_ref, aligned_agent)
    ssim_info["temporal_offset"] = offset

    phash_score, phash_info = compute_phash_similarity(aligned_ref, aligned_agent)

    dur_score, dur_info = compute_duration_penalty(len(ref_frames), len(agent_frames))

    score = round(ssim_score * phash_score * dur_score, 4)

    write_reward(args.output_dir, score,
        [{"subtask": "ssim_gated", "score": round(ssim_score, 6)},
         {"subtask": "phash_similarity", "score": round(phash_score, 6)},
         {"subtask": "duration", "score": round(dur_score, 6)}],
        {"ssim_info": ssim_info, "phash_info": phash_info,
         "duration_info": dur_info, "temporal_offset": offset})


if __name__ == "__main__":
    main()
