FROM node:22-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git tmux strace \
        ffmpeg \
        chromium \
        fonts-liberation \
        libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
        libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
        libpango-1.0-0 libcairo2 libasound2 \
        python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Python deps for verifier (opencv + scikit-image for video comparison)
RUN pip3 install --break-system-packages --no-cache-dir \
    opencv-python-headless==4.11.0.86 scikit-image==0.25.2 numpy==2.2.6

RUN useradd --create-home --shell /bin/bash agent

# Workaround: Harbor's oracle agent pre-creates oracle.txt on the host
# (owned by ubuntu:docker, 0664). Bind-mounted into the container, the
# "agent" user (uid 1001) falls into "other" and can only read it. The
# redirect in `bash -c "solve.sh > oracle.txt"` then fails. BASH_ENV is
# sourced by non-interactive bash before redirections are processed, so
# we delete the stale file here; the redirect re-creates it owned by agent.
RUN printf '#!/bin/bash\nrm -f /logs/agent/oracle.txt 2>/dev/null || true\n' \
      > /usr/local/lib/fix_oracle_perms.sh && \
    chmod +r /usr/local/lib/fix_oracle_perms.sh
ENV BASH_ENV=/usr/local/lib/fix_oracle_perms.sh

RUN mkdir -p /tests && chmod 700 /tests
RUN mkdir -p /solution && chown agent:agent /solution

WORKDIR /app
COPY workspace/ /app/

# Install node_modules at build time (no internet during agent run)
RUN npm ci && npx puppeteer browsers install chrome

# Render reference video from source scene at build time
COPY source_scene.tsx /tmp/source_scene.tsx
RUN cp /app/src/project.tsx /tmp/agent_stub.tsx && \
    cp /tmp/source_scene.tsx /app/src/project.tsx && \
    npm run render && \
    test -s /app/output/video.mp4 && \
    mv /app/output/video.mp4 /app/reference.mp4 && \
    rm -rf /app/output /app/dist && \
    cp /tmp/agent_stub.tsx /app/src/project.tsx && \
    rm /tmp/source_scene.tsx /tmp/agent_stub.tsx

# Pristine snapshot + reference video into /tests/ (root-owned, agent can't touch)
# Harbor uploads tests/ via docker-cp merge — existing files survive.
RUN tar --exclude='./reference.mp4' --exclude='./node_modules' \
    -cf /tests/pristine_app.tar -C /app . && \
    cp -a /app/node_modules /tests/node_modules_backup && \
    cp /app/reference.mp4 /tests/reference.mp4

# Bake solution into image (docker-compose cp can be unreliable)
COPY solve.sh /solution/solve.sh
COPY solution_project.tsx /solution/project.tsx
RUN chmod +x /solution/solve.sh

RUN chmod 700 /tests
RUN chown -R agent:agent /app
