FROM python:3.11-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.4.30 /uv /uvx /bin/

RUN useradd -m karamazov_user          # create user first

WORKDIR /app

COPY --chown=karamazov_user pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY --chown=karamazov_user ./app ./app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

USER karamazov_user

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]