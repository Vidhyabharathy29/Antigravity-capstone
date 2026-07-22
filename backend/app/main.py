import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from .data_fetcher import fetch_stock_data, fetch_stock_info
from .indicators import add_all_indicators
from .ts_models import fit_and_forecast_arima
from .ml_models import train_and_evaluate_ml

app = FastAPI(
    title="Stock Market Analytics & ML Prediction API",
    description="Backend API for fetching stock data, computing technical indicators, running ARIMA forecasts, and training ML classifiers.",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend port (e.g., http://localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MLTrainRequest(BaseModel):
    ticker: str
    model_type: str = "rf"
    n_estimators: int = 100
    max_depth: int = 6
    lags: int = 5
    test_size: float = 0.2

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reset index, format date column to YYYY-MM-DD, and replace NaNs/Infs with None for JSON serialization.
    """
    df = df.copy()
    
    # Identify index column (usually 'Date' or 'Datetime')
    if df.index.name is not None:
        index_name = df.index.name
    else:
        index_name = "Date"
        
    df = df.reset_index()
    
    # Rename the date/index column if needed
    if index_name in df.columns:
        df = df.rename(columns={index_name: "Date"})
    elif "index" in df.columns:
        df = df.rename(columns={"index": "Date"})
        
    # Format dates
    try:
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    except Exception:
        df["Date"] = df["Date"].astype(str)
        
    # Replace NaN, Inf, -Inf with None for standard JSON compliance
    return df.to_dict(orient="records")

def sanitize_records(records: list) -> list:
    cleaned = []
    for row in records:
        clean_row = {}
        for k, v in row.items():
            if isinstance(v, float) and (np.isnan(v) or np.isinf(v)):
                clean_row[k] = None
            elif isinstance(v, (pd.Timestamp, pd.Timedelta)):
                clean_row[k] = str(v)
            else:
                clean_row[k] = v
        cleaned.append(clean_row)
    return cleaned

@app.get("/")
def read_root():
    return {"status": "online", "message": "Stock Prediction API is running."}

@app.get("/api/stock/info")
def get_stock_info(ticker: str = Query(..., description="Stock ticker symbol, e.g. AAPL")):
    ticker = ticker.upper().strip()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker symbol cannot be empty.")
    
    info = fetch_stock_info(ticker)
    return info

@app.get("/api/stock/history")
def get_stock_history(
    ticker: str = Query(..., description="Stock ticker symbol, e.g. AAPL"),
    period: str = Query("2y", description="Time period, e.g. 1mo, 6mo, 1y, 2y, 5y")
):
    ticker = ticker.upper().strip()
    df = fetch_stock_data(ticker, period)
    
    if df is None or df.empty:
        raise HTTPException(
            status_code=404, 
            detail=f"No stock data found for ticker '{ticker}' and period '{period}'."
        )
        
    # Calculate indicators
    df_with_indicators = add_all_indicators(df)
    
    # Clean for JSON serialization
    raw_records = clean_dataframe(df_with_indicators)
    records = sanitize_records(raw_records)
    
    return {
        "ticker": ticker,
        "period": period,
        "count": len(records),
        "data": records
    }

@app.get("/api/forecast")
def get_forecast(
    ticker: str = Query(..., description="Stock ticker symbol, e.g. AAPL"),
    p: int = Query(1, description="ARIMA autoregressive order (p)"),
    d: int = Query(1, description="ARIMA differencing order (d)"),
    q: int = Query(1, description="ARIMA moving average order (q)"),
    steps: int = Query(30, description="Number of days to forecast")
):
    ticker = ticker.upper().strip()
    df = fetch_stock_data(ticker, "2y")  # Use 2 years historical data to fit
    
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail=f"No stock data found to build forecast for '{ticker}'.")
        
    close_series = df["Close"]
    forecast_results = fit_and_forecast_arima(close_series, p, d, q, forecast_steps=steps)
    
    return forecast_results

@app.post("/api/train_ml")
def train_machine_learning(req: MLTrainRequest):
    ticker = req.ticker.upper().strip()
    # Fetch historical data (use max 2y or 5y for training depending on request, 2y is standard and fast)
    df = fetch_stock_data(ticker, "2y")
    
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail=f"No stock data found to train ML model for '{ticker}'.")
        
    results = train_and_evaluate_ml(
        df=df,
        model_type=req.model_type,
        n_estimators=req.n_estimators,
        max_depth=req.max_depth,
        lags=req.lags,
        test_size=req.test_size
    )
    
    if not results.get("success", False):
        raise HTTPException(status_code=400, detail=results.get("error", "ML training failed."))
        
    return results
