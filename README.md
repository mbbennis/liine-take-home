# Restaurant open-hours API

Take-home implementation of [this prompt](https://gist.github.com/sharpmoose/d25487b913a08f6a6e6059c07035a041#file-restaurants-csv).

Single-endpoint Flask service that returns the list of restaurants open at a given timestamp. Hours are parsed from `data/restaurants.csv` at startup into a precomputed minute-of-week lookup table, so queries are O(1).

## Setup

Requires [uv](https://docs.astral.sh/uv/). Then:

```sh
make install-dev   # or: uv sync --group dev
```

## Run

Dev server (port 5000):

```sh
make run           # or: uv run flask --app app run
```

Or via Docker (port 8000):

```sh
make docker-run    # builds the image and runs it
```

## Test

```sh
make test          # unit + integration (fast)
make test-e2e      # builds the image, runs container tests
```

## API

`GET /restaurants?at=<iso8601>` — returns restaurants open at that local time.

```sh
curl "http://localhost:5000/restaurants?at=2026-05-18T23:00:00"
```

```json
[
    {"name": "Caffe Luna"},
    {"name": "Bonchon"},
    {"name": "Seoul 116"},
    {"name": "Stanbury"},
    {"name": "42nd Street Oyster Bar"}
]
```

Returns `400` if `at` is missing or not a parseable ISO 8601 timestamp.

## Configuration

`RESTAURANT_CSV` env var overrides the default CSV path (`./data/restaurants.csv`).
