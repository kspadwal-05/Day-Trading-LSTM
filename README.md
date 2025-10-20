# Day Trading LSTM Platform

A comprehensive AI-powered day trading platform that combines LSTM neural networks with technical analysis for stock price prediction and automated trading signals.

## 🚀 Features

- **LSTM Price Forecasting**: Deep learning models to predict future stock prices
- **Technical Analysis**: EMA crossovers, RSI, Bollinger Bands indicators
- **Trading Signals**: Automated buy/sell signal generation
- **Backtesting**: Historical strategy performance evaluation
- **Real-time Data**: Live stock data integration via yfinance
- **Web Dashboard**: Modern, responsive web interface

## 🛠️ Technologies

### Backend
- **FastAPI**: Modern, fast web framework for APIs
- **TensorFlow/Keras**: Deep learning and LSTM models
- **Pandas/NumPy**: Data manipulation and analysis
- **Scikit-learn**: Machine learning utilities
- **yfinance**: Real-time stock data

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Interactive dashboard
- **Chart.js**: Data visualization

## 📁 Project Structure

```
Day-Trading-LSTM/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── routers/                # API endpoints
│   │   ├── data.py            # Historical data endpoints
│   │   ├── forecast.py        # Prediction endpoints
│   │   ├── signals.py         # Trading signals
│   │   └── backtest.py        # Strategy backtesting
│   └── services/              # Business logic
│       ├── data_service.py    # Data fetching
│       ├── model_service.py   # LSTM training/inference
│       ├── signals_service.py # Technical indicators
│       └── backtest_service.py # Strategy evaluation
├── frontend/
│   └── index.html             # Web dashboard
├── models/                    # Trained LSTM models
├── requirements.txt           # Python dependencies
├── run_backend.py            # Backend startup script
├── run_frontend.py           # Frontend startup script
└── LSTM_Based_Forecasting.ipynb # Original research notebook
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend

```bash
python run_backend.py
```

The API will be available at `http://localhost:8000`

### 3. Start the Frontend

```bash
python run_frontend.py
```

The dashboard will open at `http://localhost:3000`

## 📊 API Endpoints

### Data
- `GET /data/history` - Fetch historical price data
- `GET /forecast/next` - Generate price predictions
- `GET /signals/` - Get trading signals
- `GET /backtest/crossover` - Run strategy backtest

### Example Usage

```bash
# Get AAPL data for the last 7 days
curl "http://localhost:8000/data/history?symbol=AAPL&period=7d&interval=1m"

# Get 60-step price forecast
curl "http://localhost:8000/forecast/next?symbol=AAPL&horizon=60"

# Get trading signals
curl "http://localhost:8000/signals/?symbol=AAPL&fast=9&slow=21"

# Run backtest
curl "http://localhost:8000/backtest/crossover?symbol=AAPL&period=6mo"
```

## 🧠 LSTM Model

The LSTM model uses:
- **Architecture**: 2-layer LSTM with dropout
- **Input**: 60 timesteps of price data
- **Output**: Next price prediction
- **Training**: Adam optimizer, MSE loss
- **Features**: Close price normalization

## 📈 Trading Signals

### Technical Indicators
- **EMA Crossovers**: Fast/Slow exponential moving averages
- **RSI**: Relative Strength Index (oversold/overbought)
- **Bollinger Bands**: Price volatility indicators

### Signal Types
- `EMA_BULLISH_CROSSOVER`: Fast EMA crosses above slow EMA
- `EMA_BEARISH_CROSSOVER`: Fast EMA crosses below slow EMA
- `RSI_OVERSOLD`: RSI < 30 (potential buy)
- `RSI_OVERBOUGHT`: RSI > 70 (potential sell)
- `BB_OVERSOLD`: Price below lower Bollinger Band
- `BB_OVERBOUGHT`: Price above upper Bollinger Band

## 🔄 Backtesting

The platform includes a comprehensive backtesting engine that evaluates:
- **Total Return**: Percentage gain/loss
- **Win Rate**: Percentage of profitable trades
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Profit Factor**: Ratio of gross profit to gross loss
- **Trade Statistics**: Average win/loss, total trades

## ⚠️ Disclaimer

This platform is for educational and research purposes only. Past performance does not guarantee future results. Always do your own research before making investment decisions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.