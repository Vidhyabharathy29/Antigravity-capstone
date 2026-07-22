import pandas as pd
import numpy as np

def compute_sma(series: pd.Series, window: int = 20) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA).
    """
    return series.rolling(window=window).mean()

def compute_ema(series: pd.Series, window: int = 20) -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA).
    """
    return series.ewm(span=window, adjust=False).mean()

def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    """
    delta = series.diff()
    
    # Get gains and losses
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    # Use Wilder's exponential smoothing method
    avg_gain = gain.ewm(alpha=1/window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/window, adjust=False).mean()
    
    # Avoid division by zero
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    
    # Fill leading NaNs or zeroes
    return rsi.fillna(50)  # Default neutral value is 50

def compute_macd(series: pd.Series, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> pd.DataFrame:
    """
    Calculate Moving Average Convergence Divergence (MACD).
    Returns a DataFrame with columns: macd, signal, histogram.
    """
    ema_fast = series.ewm(span=fast_period, adjust=False).mean()
    ema_slow = series.ewm(span=slow_period, adjust=False).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    
    return pd.DataFrame({
        "macd": macd_line,
        "signal": signal_line,
        "histogram": macd_histogram
    }, index=series.index)

def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add standard technical indicators to a stock DataFrame in place.
    Requires a 'Close' column.
    """
    if "Close" not in df.columns:
        raise ValueError("DataFrame must contain a 'Close' column.")
        
    df = df.copy()
    close = df["Close"]
    
    df["SMA_20"] = compute_sma(close, window=20)
    df["SMA_50"] = compute_sma(close, window=50)
    df["EMA_20"] = compute_ema(close, window=20)
    df["EMA_50"] = compute_ema(close, window=50)
    df["RSI_14"] = compute_rsi(close, window=14)
    
    macd_df = compute_macd(close)
    df["MACD"] = macd_df["macd"]
    df["MACD_Signal"] = macd_df["signal"]
    df["MACD_Hist"] = macd_df["histogram"]
    
    # Fill NaN values with backfill then forwardfill to ensure API responses are clean
    df = df.bfill().ffill()
    
    return df
