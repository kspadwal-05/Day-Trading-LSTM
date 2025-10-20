import yfinance as yf
import pandas as pd
from typing import Optional


def fetch_price_history(symbol: str, period: str = "7d", interval: str = "1m") -> pd.DataFrame:
    """
    Fetch historical price data for a given symbol.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
        period: Data period (e.g., '7d', '1mo', '3mo', '1y')
        interval: Data interval (e.g., '1m', '5m', '15m', '1h', '1d')
    
    Returns:
        DataFrame with OHLCV data
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval)
        
        if data.empty:
            raise ValueError(f"No data found for symbol {symbol}")
            
        return data
    except Exception as e:
        raise ValueError(f"Error fetching data for {symbol}: {str(e)}")
