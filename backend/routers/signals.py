from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.data_service import fetch_price_history
from services.signals_service import generate_signals

router = APIRouter()


class SignalsResponse(BaseModel):
    symbol: str
    signals: list[dict]


@router.get("/")
def get_signals(
    symbol: str = Query(...),
    period: str = Query("1mo"),
    interval: str = Query("1h"),
    fast: int = Query(9),
    slow: int = Query(21),
):
    df = fetch_price_history(symbol=symbol, period=period, interval=interval)
    signals = generate_signals(df=df, fast=fast, slow=slow)
    return SignalsResponse(symbol=symbol, signals=signals)
