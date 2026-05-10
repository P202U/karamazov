FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# 1. Install system dependencies (FFmpeg for audio)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Install dependencies using uv
# Enable bytecode compilation for faster startups
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy only what's needed to install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# 3. Final Stage
COPY . .
# Sync the rest of the project
RUN uv sync --frozen --no-dev

# Path to the virtualenv created by uv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]