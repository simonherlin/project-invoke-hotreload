FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /workspace
COPY . /workspace
RUN uv sync --project /workspace/services/api-b
