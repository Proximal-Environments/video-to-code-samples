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

_check 'node --version'                                    'node'
_check 'npx tsc --version'                                 'typescript'
_check 'which chromium || which chromium-browser'           'chromium'
_check 'which ffmpeg'                                       'ffmpeg'
_check 'which ffprobe'                                      'ffprobe'
_check 'test -f /app/reference.mp4'                         'reference.mp4 present'
_check 'test -f /app/src/project.tsx'                       'project.tsx present'
_check 'node -e "require(\"@revideo/core\")"'               'revideo/core'
_check 'node -e "require(\"@revideo/2d\")"'                 'revideo/2d'
_check 'node -e "require(\"@revideo/renderer\")"'           'revideo/renderer'

echo "[oracle:tools] END  ok=$_ok fail=$_fail"
[ "$_fail" -eq 0 ] || \
    echo "[oracle:tools] WARNING — $_fail tool(s) unreachable; task may be unfair to agents"

# === Reference solution. Must score 1.0. ===
set -e
cp /solution/project.tsx /app/src/project.tsx
cd /app
npm run render
