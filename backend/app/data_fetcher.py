import os
import pandas as pd
import yfinance as yf
from typing import Dict, Any, Optional

# Local cache directory inside the workspace
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_stock_data(ticker_symbol: str, period: str = "2y") -> Optional[pd.DataFrame]:
    """
    Fetch historical stock data from Yahoo Finance and cache it locally.
    
    Parameters:
    - ticker_symbol: e.g. "AAPL", "MSFT"
    - period: e.g. "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    """
    ticker_symbol = ticker_symbol.upper().strip()
    cache_file = os.path.join(CACHE_DIR, f"{ticker_symbol}_{period}.csv")
    
    # Simple check for file cache modification time (refresh cache if older than 6 hours)
    if os.path.exists(cache_file):
        import time
        file_age = time.time() - os.path.getmtime(cache_file)
        if file_age < 21600:  # 6 hours
            try:
                df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
                if not df.empty:
                    return df
            except Exception:
                pass # Cache read error, download fresh data

    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period)
        if df.empty:
            return None
        
        # Save to cache
        df.to_csv(cache_file)
        return df
    except Exception as e:
        print(f"Error fetching historical data for {ticker_symbol}: {e}")
        return None

def fetch_stock_info(ticker_symbol: str) -> Dict[str, Any]:
    """
    Fetch metadata/info about a specific ticker.
    """
    ticker_symbol = ticker_symbol.upper().strip()
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Select important keys, provide defaults if they don't exist
        return {
            "symbol": ticker_symbol,
            "companyName": info.get("longName", ticker_symbol),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "marketCap": info.get("marketCap", 0),
            "peRatio": info.get("trailingPE", None),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh", 0.0),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow", 0.0),
            "regularMarketPrice": info.get("currentPrice", info.get("regularMarketPreviousClose", 0.0)),
            "currency": info.get("currency", "USD"),
            "summary": info.get("longBusinessSummary", "")
        }
    except Exception as e:
        print(f"Error fetching info for {ticker_symbol}: {e}")
        return {
            "symbol": ticker_symbol,
            "companyName": ticker_symbol,
            "sector": "N/A",
            "industry": "N/A",
            "marketCap": 0,
            "peRatio": None,
            "fiftyTwoWeekHigh": 0.0,
            "fiftyTwoWeekLow": 0.0,
            "regularMarketPrice": 0.0,
            "currency": "USD",
            "summary": f"Could not retrieve details for ticker {ticker_symbol}."
        }
