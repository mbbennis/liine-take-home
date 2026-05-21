FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /srv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY app ./app
COPY data ./data

EXPOSE 8000

CMD [".venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()"]
