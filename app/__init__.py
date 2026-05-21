import os
from pathlib import Path

from flask import Flask

from .index import build_index
from .parser import load_restaurants
from .routes import bp

DEFAULT_CSV = Path(__file__).parent.parent / "data" / "restaurants.csv"


def create_app() -> Flask:
    csv_path = os.environ.get("RESTAURANT_CSV") or DEFAULT_CSV
    app = Flask(__name__)
    restaurants = load_restaurants(csv_path)
    app.restaurant_index = build_index(restaurants)
    app.register_blueprint(bp)
    return app
