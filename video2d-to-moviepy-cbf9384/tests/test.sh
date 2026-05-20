#!/bin/bash
VERIFIER_DIR="/logs/verifier"
TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
SCORER_PYTHON="$TESTS_DIR/.venv/bin/python"

chmod 700 "$VERIFIER_DIR"
rm -rf "$VERIFIER_DIR"/*

fail_with() {
    $SCORER_PYTHON "$TESTS_DIR/compute_reward.py" --fail "$1" --output-dir "$VERIFIER_DIR" 2>/dev/null \
        || echo '{"score": 0.0, "subscores": [], "additional_data": {"reason": "'"$1"'"}}' > "$VERIFIER_DIR/reward.json"
    echo "0.0" > "$VERIFIER_DIR/reward.txt"
    echo "FAIL: $1"
    exit 0
}

[ ! -f /app/scene.py ] && fail_with "scene_not_found"
[ ! -f /tests/reference.mp4 ] && fail_with "no_reference_video"

# Source-level anti-cheat on scene.py only (the deliverable).
if grep -qE 'cv2\.VideoCapture|cv2\.imread|open\s*\(|\.read_bytes|\.read_text|subprocess|os\.system|os\.popen|os\.exec|Image\.open|\bexec\s*\(|\beval\s*\(|\bcompile\s*\(|__import__|getattr|base64|zlib|gzip|bz2|lzma|pickle|marshal|codecs|binascii|urllib|requests|http\.|socket|ctypes|cffi|importlib|VideoFileClip|AudioFileClip|shutil|json\.loads|json\.load|np\.load|np\.fromfile|np\.loadtxt|np\.memmap|np\.genfromtxt|FFMPEG_VideoReader' /app/scene.py; then
    grep -nE 'cv2\.VideoCapture|cv2\.imread|open\s*\(|\.read_bytes|\.read_text|subprocess|os\.system|os\.popen|os\.exec|Image\.open|\bexec\s*\(|\beval\s*\(|\bcompile\s*\(|__import__|getattr|base64|zlib|gzip|bz2|lzma|pickle|marshal|codecs|binascii|urllib|requests|http\.|socket|ctypes|cffi|importlib|VideoFileClip|AudioFileClip|shutil|json\.loads|json\.load|np\.load|np\.fromfile|np\.loadtxt|np\.memmap|np\.genfromtxt|FFMPEG_VideoReader' /app/scene.py \
        > "$VERIFIER_DIR/cheat-matches.txt" 2>&1 || true
    fail_with "cheat_pattern_detected"
fi

cp /app/scene.py /run/verified_scene.py || fail_with "snapshot_failed"
chmod a+r /run/verified_scene.py

# Clean-room: wipe all writable surfaces using find (catches dotfiles
# like ..x that glob-based rm -rf misses), restore from pristine tarball.
find /app -mindepth 1 -delete
find /home/agent -mindepth 1 -delete 2>/dev/null || true
find /solution -mindepth 1 -delete 2>/dev/null || true
find /tmp /dev/shm /var/tmp -mindepth 1 -delete 2>/dev/null || true
tar xf /tests/pristine_app.tar -C /app || fail_with "pristine_restore_failed"
chown -R agent:agent /app
cp /run/verified_scene.py /app/scene.py
chown agent:agent /app/scene.py

pkill -9 -u agent 2>/dev/null || true
sleep 0.5

# strace -f blocks until all forked children exit. We don't inspect the
# log — Pristine restore + reference removal + source grep are the
# anti-cheat; strace just prevents background processes from outliving
# the render.
strace -f -e trace=openat \
    -o "$VERIFIER_DIR/strace.log" \
    timeout 300 \
    su agent -c 'cd /app && uv run python scene.py > /dev/null 2>&1'

[ ! -f /app/output.mp4 ] && fail_with "no_output_video"
[ -L /app/output.mp4 ] && fail_with "output_is_symlink"
cp /app/output.mp4 /tests/agent_output.mp4

timeout 600 $SCORER_PYTHON "$TESTS_DIR/compute_reward.py" \
    --agent-video /tests/agent_output.mp4 \
    --agent-source /run/verified_scene.py \
    --output-dir "$VERIFIER_DIR" \
    2>"$VERIFIER_DIR/scorer_stderr.txt" \
    || fail_with "scorer_crashed"

exit 0
