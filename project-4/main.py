import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

def load_offline_data(filepath_or_buffer) -> pd.DataFrame:
    """
    Loads dataset from a local CSV file or uploaded file buffer.
    """
    try:
        # Skip the second header row containing ticker symbols resulting from yfinance
        data = pd.read_csv(filepath_or_buffer, skiprows=[1])
        return data
    except Exception as e:
        print(f"Error loading offline data: {e}")
        return pd.DataFrame()

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares dataset with moving averages and lag features.
    Predicts the next day's 'Close' price.
    """
    # Create copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Calculate Moving Averages
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # Lag features
    df['Close_Lag1'] = df['Close'].shift(1)
    df['Volume_Lag1'] = df['Volume'].shift(1)
    
    # Target variable (Next day's Close price)
    df['Target_Next_Close'] = df['Close'].shift(-1)
    
    # Drop NaNs that resulted from moving averages and shifts
    df.dropna(inplace=True)
    return df

def train_predictive_model(df: pd.DataFrame):
    """
    Trains a Random Forest Regressor to predict the next day's Close price
    and returns metrics and a unified DataFrame of Actuals vs Predictions.
    """
    features = ['Close', 'Open', 'High', 'Low', 'Volume', 'SMA_10', 'SMA_50', 'Close_Lag1', 'Volume_Lag1']
    
    X = df[features]
    y = df['Target_Next_Close']
    
    # Use 80% for training and 20% for testing, but keep order for time series context
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    
    # Create output dataframe for visualization
    results_df = df[split_idx:].copy()
    results_df['Predicted_Next_Close'] = predictions
    results_df['Actual_Next_Close'] = y_test
    
    metrics = {
        "MSE": mse,
        "MAE": mae,
        "Accuracy_Score_approx": model.score(X_test, y_test) # R^2 score
    }
    
    return results_df, metrics
