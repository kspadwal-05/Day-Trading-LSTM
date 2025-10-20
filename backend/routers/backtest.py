from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.data_service import fetch_price_history
from services.backtest_service import run_crossover_backtest

router = APIRouter()


class BacktestResponse(BaseModel):
    symbol: str
    period: str
    interval: str
    summary: dict
    equity_curve: list[float]


@router.get("/crossover")
def crossover_backtest(
    symbol: str = Query(...),
    period: str = Query("6mo"),
    interval: str = Query("1h"),
    fast: int = Query(9),
    slow: int = Query(21),
):
    df = fetch_price_history(symbol=symbol, period=period, interval=interval)
    summary, equity_curve = run_crossover_backtest(df=df, fast=fast, slow=slow)
    return BacktestResponse(symbol=symbol, period=period, interval=interval, summary=summary, equity_curve=list(map(float, equity_curve)))
