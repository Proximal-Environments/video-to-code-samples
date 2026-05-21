#!/bin/bash
VERIFIER_DIR="/logs/verifier"
TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
SCORER_PYTHON="python3"

chmod 700 "$VERIFIER_DIR"
rm -rf "$VERIFIER_DIR"/*

fail_with() {
    $SCORER_PYTHON "$TESTS_DIR/compute_reward.py" --fail "$1" --output-dir "$VERIFIER_DIR" 2>/dev/null \
        || echo '{"score": 0.0, "subscores": [], "additional_data": {"reason": "'"$1"'"}}' > "$VERIFIER_DIR/reward.json"
    echo "0.0" > "$VERIFIER_DIR/reward.txt"
    echo "FAIL: $1"
    exit 0
}

[ ! -f /app/src/project.tsx ] && fail_with "project_tsx_not_found"
[ ! -f /tests/reference.mp4 ] && fail_with "no_reference_video"

# Source-level anti-cheat on project.tsx (the deliverable).
# Block: file I/O, exec/eval, subprocess, video reading, data extraction
if grep -qE 'readFileSync|readFile|writeFileSync|createReadStream|\bfs\.|child_process|execSync|spawnSync|spawn\(|exec\(|\.fork\(|eval\(|Function\(|require\(.fs|import.*from.*fs|VideoCapture|ffmpeg|fluent-ffmpeg|\bsharp\b|jimp|Jimp|\bdecode\b|\bencode\b|base64|Buffer\.from|atob|btoa' /app/src/project.tsx; then
    grep -nE 'readFileSync|readFile|writeFileSync|createReadStream|\bfs\.|child_process|execSync|spawnSync|spawn\(|exec\(|\.fork\(|eval\(|Function\(|require\(.fs|import.*from.*fs|VideoCapture|ffmpeg|fluent-ffmpeg|\bsharp\b|jimp|Jimp|\bdecode\b|\bencode\b|base64|Buffer\.from|atob|btoa' /app/src/project.tsx \
        > "$VERIFIER_DIR/cheat-matches.txt" 2>&1 || true
    fail_with "cheat_pattern_detected"
fi

cp /app/src/project.tsx /run/verified_project.tsx || fail_with "snapshot_failed"
chmod a+r /run/verified_project.tsx

# Clean-room: wipe all writable surfaces, restore from pristine tarball.
find /app -mindepth 1 -not -path '*/node_modules/*' -delete 2>/dev/null || true
find /home/agent -mindepth 1 -delete 2>/dev/null || true
find /solution -mindepth 1 -delete 2>/dev/null || true
find /tmp /dev/shm /var/tmp -mindepth 1 -delete 2>/dev/null || true
tar xf /tests/pristine_app.tar -C /app || fail_with "pristine_restore_failed"
# Restore node_modules if needed
[ ! -d /app/node_modules ] && cp -a /tests/node_modules_backup /app/node_modules
chown -R agent:agent /app
cp /run/verified_project.tsx /app/src/project.tsx
chown agent:agent /app/src/project.tsx

pkill -9 -u agent 2>/dev/null || true
sleep 0.5

# Render under strace — blocks until all forked children exit.
strace -f -e trace=openat \
    -o "$VERIFIER_DIR/strace.log" \
    timeout 600 \
    su agent -c 'cd /app && npm run render > /dev/null 2>&1'

# Audit strace log for reward file manipulation attempts.
if grep -qE 'openat\(.*reward\.(txt|json).*O_WRONLY' "$VERIFIER_DIR/strace.log" 2>/dev/null; then
    fail_with "strace_reward_write_detected"
fi

[ ! -f /app/output/video.mp4 ] && fail_with "no_output_video"
[ -L /app/output/video.mp4 ] && fail_with "output_is_symlink"
cp /app/output/video.mp4 /tests/agent_output.mp4

timeout 600 $SCORER_PYTHON "$TESTS_DIR/compute_reward.py" \
    --agent-video /tests/agent_output.mp4 \
    --agent-source /run/verified_project.tsx \
    --output-dir "$VERIFIER_DIR" \
    2>"$VERIFIER_DIR/scorer_stderr.txt" \
    || fail_with "scorer_crashed"

exit 0
