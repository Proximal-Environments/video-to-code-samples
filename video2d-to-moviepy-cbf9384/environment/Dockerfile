FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git tmux strace \
        ffmpeg \
        libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd --create-home --shell /bin/bash agent

RUN mkdir -p /tests
RUN mkdir -p /solution && chown agent:agent /solution

# Render reference video at build time from source scene.
COPY source_scene.py /tmp/source_scene.py

WORKDIR /app
COPY workspace/ /app/

RUN uv sync --no-install-project

RUN /app/.venv/bin/python /tmp/source_scene.py && \
    test -s /app/output.mp4 && \
    mv /app/output.mp4 /app/reference.mp4

# Scorer venv + pristine snapshot into /tests/ (root-owned, agent can't touch).
# Excludes reference.mp4 so pristine restore doesn't leak it back.
RUN cp -a /app/.venv /tests/.venv && \
    tar --exclude='./reference.mp4' -cf /tests/pristine_app.tar -C /app .

# Verifier assets
COPY tests/ /tests/
RUN cp /app/reference.mp4 /tests/reference.mp4 && \
    cd /tests && /tests/.venv/bin/python precompute_ref.py /tmp/source_scene.py /tests/gate_thresholds.json && \
    rm -f /tmp/source_scene.py

RUN chmod 700 /tests
RUN chown -R agent:agent /app
