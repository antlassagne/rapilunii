FROM ghcr.io/astral-sh/uv:debian
COPY . .
RUN uv venv --seed
RUN uv sync
