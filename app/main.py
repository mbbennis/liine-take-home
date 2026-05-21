import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from .index import build_index, minute_of_week
from .parser import load_restaurants

DEFAULT_CSV = Path(__file__).parent.parent / "data" / "restaurants.csv"


@asynccontextmanager
async def lifespan(app: FastAPI):
    csv_path = os.environ.get("RESTAURANT_CSV") or DEFAULT_CSV
    restaurants = load_restaurants(csv_path)
    app.state.restaurant_index = build_index(restaurants)
    yield


app = FastAPI(lifespan=lifespan)


class RestaurantName(BaseModel):
    name: str


@app.get("/restaurants", response_model=list[RestaurantName])
def get_open_restaurants(request: Request, at: str | None = None):
    if not at:
        raise HTTPException(status_code=400, detail="missing 'at' query parameter")
    try:
        dt = datetime.fromisoformat(at)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="'at' must be an ISO 8601 timestamp"
        )

    names = request.app.state.restaurant_index[minute_of_week(dt)]
    return [{"name": n} for n in names]
