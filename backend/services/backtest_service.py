import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
from services.signals_service import generate_signals


def run_crossover_backtest(df: pd.DataFrame, fast: int = 9, slow: int = 21, 
                          initial_capital: float = 10000.0) -> Tuple[Dict, List[float]]:
    """Run backtest for EMA crossover strategy."""
    
    # Generate signals
    signals_data = generate_signals(df, fast, slow)
    
    # Initialize backtest variables
    capital = initial_capital
    position = 0  # 0 = no position, 1 = long, -1 = short
    shares = 0
    equity_curve = [capital]
    
    # Track trades
    trades = []
    current_trade = None
    
    for signal_data in signals_data:
        timestamp = signal_data['timestamp']
        price = signal_data['price']
        signals = signal_data['signals']
        
        # Check for EMA crossover signals
        if 'EMA_BULLISH_CROSSOVER' in signals and position <= 0:
            # Enter long position
            if position == -1:  # Close short position
                pnl = shares * (current_trade['entry_price'] - price)
                capital += pnl
                trades.append({
                    'entry_time': current_trade['entry_time'],
                    'exit_time': timestamp,
                    'entry_price': current_trade['entry_price'],
                    'exit_price': price,
                    'shares': shares,
                    'pnl': pnl,
                    'type': 'SHORT'
                })
                shares = 0
                position = 0
            
            # Open long position
            shares = capital / price
            capital = 0
            position = 1
            current_trade = {
                'entry_time': timestamp,
                'entry_price': price
            }
        
        elif 'EMA_BEARISH_CROSSOVER' in signals and position >= 0:
            # Enter short position
            if position == 1:  # Close long position
                pnl = shares * (price - current_trade['entry_price'])
                capital = shares * price
                trades.append({
                    'entry_time': current_trade['entry_time'],
                    'exit_time': timestamp,
                    'entry_price': current_trade['entry_price'],
                    'exit_price': price,
                    'shares': shares,
                    'pnl': pnl,
                    'type': 'LONG'
                })
                shares = 0
                position = 0
            
            # Open short position
            shares = capital / price
            capital = 0
            position = -1
            current_trade = {
                'entry_time': timestamp,
                'entry_price': price
            }
        
        # Calculate current equity
        if position == 1:  # Long position
            current_equity = shares * price
        elif position == -1:  # Short position
            current_equity = capital + shares * (current_trade['entry_price'] - price)
        else:  # No position
            current_equity = capital
        
        equity_curve.append(current_equity)
    
    # Close any open position
    if position != 0:
        last_price = df['Close'].iloc[-1]
        if position == 1:  # Close long
            pnl = shares * (last_price - current_trade['entry_price'])
            capital = shares * last_price
            trades.append({
                'entry_time': current_trade['entry_time'],
                'exit_time': df.index[-1].isoformat() if hasattr(df.index[-1], 'isoformat') else str(df.index[-1]),
                'entry_price': current_trade['entry_price'],
                'exit_price': last_price,
                'shares': shares,
                'pnl': pnl,
                'type': 'LONG'
            })
        elif position == -1:  # Close short
            pnl = shares * (current_trade['entry_price'] - last_price)
            capital += pnl
            trades.append({
                'entry_time': current_trade['entry_time'],
                'exit_time': df.index[-1].isoformat() if hasattr(df.index[-1], 'isoformat') else str(df.index[-1]),
                'entry_price': current_trade['entry_price'],
                'exit_price': last_price,
                'shares': shares,
                'pnl': pnl,
                'type': 'SHORT'
            })
    
    # Calculate performance metrics
    final_equity = equity_curve[-1]
    total_return = (final_equity - initial_capital) / initial_capital * 100
    
    # Calculate trade statistics
    winning_trades = [t for t in trades if t['pnl'] > 0]
    losing_trades = [t for t in trades if t['pnl'] < 0]
    
    win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
    avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
    avg_loss = np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0
    
    # Calculate maximum drawdown
    peak = initial_capital
    max_drawdown = 0
    for equity in equity_curve:
        if equity > peak:
            peak = equity
        drawdown = (peak - equity) / peak * 100
        max_drawdown = max(max_drawdown, drawdown)
    
    summary = {
        'initial_capital': initial_capital,
        'final_equity': final_equity,
        'total_return_pct': round(total_return, 2),
        'total_trades': len(trades),
        'winning_trades': len(winning_trades),
        'losing_trades': len(losing_trades),
        'win_rate_pct': round(win_rate, 2),
        'avg_win': round(avg_win, 2),
        'avg_loss': round(avg_loss, 2),
        'max_drawdown_pct': round(max_drawdown, 2),
        'profit_factor': round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0
    }
    
    return summary, equity_curve
