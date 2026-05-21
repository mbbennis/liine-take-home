from datetime import datetime

from flask import Blueprint, current_app, jsonify, request

from .index import minute_of_week

bp = Blueprint("restaurants", __name__)


@bp.route("/restaurants")
def get_open_restaurants():
    raw = request.args.get("at")
    if not raw:
        return jsonify(error="missing 'at' query parameter"), 400
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return jsonify(error="'at' must be an ISO 8601 timestamp"), 400

    names = current_app.restaurant_index[minute_of_week(dt)]
    return jsonify([{"name": n} for n in names])
