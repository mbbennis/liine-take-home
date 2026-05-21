import httpx
import pytest

pytestmark = pytest.mark.e2e


def test_happy_path_returns_open_restaurants(base_url):
    # Tuesday 7pm: typical dinner hour
    r = httpx.get(f"{base_url}/restaurants", params={"at": "2026-05-19T19:00:00"})
    assert r.status_code == 200
    names = {item["name"] for item in r.json()}
    assert "Death and Taxes" in names  # Mon-Sun 5pm-10pm
    assert "The Cowfish Sushi Burger Bar" in names  # Mon-Sun 11am-10pm


def test_excludes_just_closed_restaurant(base_url):
    # 4am on Tuesday: Seoul 116 closes at exactly 4am (half-open -> not open)
    r = httpx.get(f"{base_url}/restaurants", params={"at": "2026-05-19T04:00:00"})
    assert r.status_code == 200
    names = {item["name"] for item in r.json()}
    assert "Seoul 116" not in names


def test_response_shape_is_name_only(base_url):
    r = httpx.get(f"{base_url}/restaurants", params={"at": "2026-05-19T19:00:00"})
    items = r.json()
    assert items, "expected at least one open restaurant"
    for item in items:
        assert set(item.keys()) == {"name"}
        assert isinstance(item["name"], str) and item["name"]


def test_missing_at_returns_400(base_url):
    r = httpx.get(f"{base_url}/restaurants")
    assert r.status_code == 400


def test_bad_at_returns_400(base_url):
    r = httpx.get(f"{base_url}/restaurants", params={"at": "not-a-date"})
    assert r.status_code == 400
