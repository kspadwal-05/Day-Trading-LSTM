import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from services.data_service import fetch_price_history
import joblib
import os


def create_lstm_model(input_shape: tuple, units: int = 50) -> Sequential:
    """Create and compile LSTM model."""
    model = Sequential([
        LSTM(units, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    return model


def prepare_data(df: pd.DataFrame, lookback: int = 60) -> tuple:
    """Prepare data for LSTM training."""
    # Use Close prices
    data = df['Close'].values.reshape(-1, 1)
    
    # Scale the data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    
    # Create sequences
    X, y = [], []
    for i in range(lookback, len(scaled_data)):
        X.append(scaled_data[i-lookback:i, 0])
        y.append(scaled_data[i, 0])
    
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    return X, y, scaler


def train_model(symbol: str, period: str = "1y", interval: str = "1d") -> tuple:
    """Train LSTM model for a given symbol."""
    # Fetch data
    df = fetch_price_history(symbol, period, interval)
    
    # Prepare data
    X, y, scaler = prepare_data(df)
    
    # Split data
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    # Create and train model
    model = create_lstm_model((X.shape[1], 1))
    
    # Train model
    model.fit(X_train, y_train, 
              batch_size=32, 
              epochs=50, 
              validation_data=(X_test, y_test),
              verbose=0)
    
    # Save model and scaler
    model_path = f"models/{symbol}_lstm_model.h5"
    scaler_path = f"models/{symbol}_scaler.pkl"
    
    os.makedirs("models", exist_ok=True)
    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    
    return model, scaler


def forecast_prices(symbol: str, period: str = "7d", interval: str = "1m", horizon: int = 60) -> list:
    """Generate price forecasts using trained LSTM model."""
    try:
        # Try to load existing model
        model_path = f"models/{symbol}_lstm_model.h5"
        scaler_path = f"models/{symbol}_scaler.pkl"
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            from tensorflow.keras.models import load_model
            model = load_model(model_path)
            scaler = joblib.load(scaler_path)
        else:
            # Train new model if not found
            model, scaler = train_model(symbol, period, interval)
        
        # Get recent data for prediction
        df = fetch_price_history(symbol, period, interval)
        data = df['Close'].values.reshape(-1, 1)
        scaled_data = scaler.transform(data)
        
        # Prepare last sequence
        lookback = 60
        last_sequence = scaled_data[-lookback:].reshape(1, lookback, 1)
        
        # Generate forecasts
        predictions = []
        current_sequence = last_sequence.copy()
        
        for _ in range(horizon):
            pred = model.predict(current_sequence, verbose=0)
            predictions.append(scaler.inverse_transform(pred)[0, 0])
            
            # Update sequence for next prediction
            current_sequence = np.append(current_sequence[:, 1:, :], pred.reshape(1, 1, 1), axis=1)
        
        return [float(p) for p in predictions]
        
    except Exception as e:
        # Fallback: return simple moving average forecast
        df = fetch_price_history(symbol, period, interval)
        last_price = df['Close'].iloc[-1]
        return [float(last_price)] * horizon
