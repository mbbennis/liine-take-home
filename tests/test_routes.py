import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_returns_open_restaurants(client):
    # Tuesday 7pm in 2026: most dinner spots should be open
    resp = client.get("/restaurants?at=2026-05-19T19:00:00")
    assert resp.status_code == 200
    names = {item["name"] for item in resp.get_json()}
    assert "The Cowfish Sushi Burger Bar" in names  # Mon-Sun 11am-10pm
    assert "Death and Taxes" in names  # Mon-Sun 5pm-10pm


def test_excludes_closed_restaurants(client):
    # Tuesday 4am — almost everything is closed, but Seoul 116 (11am-4am) just closed
    resp = client.get("/restaurants?at=2026-05-19T04:00:00")
    assert resp.status_code == 200
    names = {item["name"] for item in resp.get_json()}
    assert "Seoul 116" not in names  # close at 4am sharp -> closed (half-open)


def test_garland_closed_monday(client):
    # Garland: Tues-Fri, Sun 11:30 am - 10 pm  /  Sat 5:30 pm - 11 pm  -> no Monday
    resp = client.get("/restaurants?at=2026-05-18T19:00:00")
    names = {item["name"] for item in resp.get_json()}
    assert "Garland" not in names


def test_missing_at_returns_400(client):
    resp = client.get("/restaurants")
    assert resp.status_code == 400


def test_bad_at_returns_400(client):
    resp = client.get("/restaurants?at=not-a-date")
    assert resp.status_code == 400
