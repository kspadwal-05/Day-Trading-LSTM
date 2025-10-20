from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.model_service import forecast_prices

router = APIRouter()


class ForecastResponse(BaseModel):
    symbol: str
    horizon: int
    predicted: list[float]


@router.get("/next")
def get_forecast(
    symbol: str = Query(...),
    horizon: int = Query(60, ge=1, le=240, description="Number of steps to predict"),
    period: str = Query("7d"),
    interval: str = Query("1m"),
):
    predicted = forecast_prices(symbol=symbol, period=period, interval=interval, horizon=horizon)
    return ForecastResponse(symbol=symbol, horizon=horizon, predicted=predicted)
