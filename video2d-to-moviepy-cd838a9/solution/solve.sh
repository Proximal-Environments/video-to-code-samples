#!/bin/bash
# === Toolchain sanity check (read by harbor-qa fairness audit) ===
cd /app 2>/dev/null || true
echo "[oracle:tools] BEGIN user=$(id -un) uid=$(id -u) PATH=$PATH"
_ok=0; _fail=0
_check() {
    if eval "$1" >/dev/null 2>&1; then
        _ok=$((_ok + 1)); echo "[oracle:tools]   ok    $2"
    else
        _fail=$((_fail + 1)); echo "[oracle:tools]   FAIL  $2  (cmd: $1)"
    fi
}

_check 'uv run python --version'                                          'python'
_check 'uv run python -c "import moviepy"'                                'python (moviepy)'
_check 'uv run python -c "import cv2"'                                    'python (opencv)'
_check 'uv run python -c "import numpy"'                                  'python (numpy)'
_check 'uv run python -c "from PIL import Image"'                         'python (pillow)'
_check 'uv run python -c "from skimage.metrics import structural_similarity"'  'python (scikit-image)'
_check 'which ffmpeg'                                                      'ffmpeg'
_check 'which ffprobe'                                                     'ffprobe'
_check 'test -f /app/reference.mp4'                                        'reference.mp4 present'

echo "[oracle:tools] END  ok=$_ok fail=$_fail"
[ "$_fail" -eq 0 ] || \
    echo "[oracle:tools] WARNING — $_fail tool(s) unreachable; task may be unfair to agents"

# === Reference solution. Must score 1.0. ===
set -e
cp /solution/scene.py /app/scene.py
cd /app
uv run python scene.py
