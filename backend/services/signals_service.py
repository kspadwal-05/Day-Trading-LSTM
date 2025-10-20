import pandas as pd
import numpy as np
from typing import List, Dict


def calculate_ema(data: pd.Series, period: int) -> pd.Series:
    """Calculate Exponential Moving Average."""
    return data.ewm(span=period).mean()


def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index."""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2) -> tuple:
    """Calculate Bollinger Bands."""
    sma = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, sma, lower_band


def generate_signals(df: pd.DataFrame, fast: int = 9, slow: int = 21) -> List[Dict]:
    """Generate trading signals based on technical indicators."""
    signals = []
    
    # Calculate indicators
    df['EMA_fast'] = calculate_ema(df['Close'], fast)
    df['EMA_slow'] = calculate_ema(df['Close'], slow)
    df['RSI'] = calculate_rsi(df['Close'])
    
    # Bollinger Bands
    bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(df['Close'])
    df['BB_upper'] = bb_upper
    df['BB_middle'] = bb_middle
    df['BB_lower'] = bb_lower
    
    # Generate signals
    for i in range(1, len(df)):
        current = df.iloc[i]
        previous = df.iloc[i-1]
        
        signal = {
            'timestamp': current.name.isoformat() if hasattr(current.name, 'isoformat') else str(current.name),
            'price': float(current['Close']),
            'ema_fast': float(current['EMA_fast']),
            'ema_slow': float(current['EMA_slow']),
            'rsi': float(current['RSI']),
            'bb_upper': float(current['BB_upper']),
            'bb_lower': float(current['BB_lower']),
            'signals': []
        }
        
        # EMA Crossover signals
        if (current['EMA_fast'] > current['EMA_slow'] and 
            previous['EMA_fast'] <= previous['EMA_slow']):
            signal['signals'].append('EMA_BULLISH_CROSSOVER')
        
        if (current['EMA_fast'] < current['EMA_slow'] and 
            previous['EMA_fast'] >= previous['EMA_slow']):
            signal['signals'].append('EMA_BEARISH_CROSSOVER')
        
        # RSI signals
        if current['RSI'] < 30:
            signal['signals'].append('RSI_OVERSOLD')
        elif current['RSI'] > 70:
            signal['signals'].append('RSI_OVERBOUGHT')
        
        # Bollinger Bands signals
        if current['Close'] < current['BB_lower']:
            signal['signals'].append('BB_OVERSOLD')
        elif current['Close'] > current['BB_upper']:
            signal['signals'].append('BB_OVERBOUGHT')
        
        signals.append(signal)
    
    return signals
