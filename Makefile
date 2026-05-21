.PHONY: install install-dev test test-e2e run docker-build docker-run

install:
	uv sync --no-dev

install-dev:
	uv sync --group dev

test:
	uv run pytest

test-e2e:
	uv run pytest tests/e2e -m e2e

run:
	uv run uvicorn app.main:app --reload

docker-build:
	docker build -t liine-take-home .

docker-run: docker-build
	docker run --rm -p 8000:8000 liine-take-home
