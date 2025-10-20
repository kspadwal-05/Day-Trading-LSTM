from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.data_service import fetch_price_history

router = APIRouter()


class PriceHistoryResponse(BaseModel):
    symbol: str
    interval: str
    df_csv: str  # CSV string for simplicity


@router.get("/history", response_model=PriceHistoryResponse)
def get_history(
    symbol: str = Query(..., description="Ticker symbol, e.g. AAPL"),
    period: str = Query("7d", description="e.g. 7d, 1mo, 3mo"),
    interval: str = Query("1m", description="e.g. 1m, 5m, 15m, 1h, 1d"),
):
    df = fetch_price_history(symbol=symbol, period=period, interval=interval)
    return PriceHistoryResponse(symbol=symbol, interval=interval, df_csv=df.to_csv(index=True))
