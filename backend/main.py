from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import data as data_router
from routers import forecast as forecast_router
from routers import signals as signals_router
from routers import backtest as backtest_router

app = FastAPI(title="Day Trading LSTM API", version="0.1.0")

# Allow any origin; no auth per requirement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


# Include feature routers
app.include_router(data_router.router, prefix="/data", tags=["data"])
app.include_router(forecast_router.router, prefix="/forecast", tags=["forecast"])
app.include_router(signals_router.router, prefix="/signals", tags=["signals"])
app.include_router(backtest_router.router, prefix="/backtest", tags=["backtest"])
