import os
import sqlite3
import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stock_market.db")

def get_connection():
    """Returns a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema and creates all required relational tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Stocks Metadata Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        symbol TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        market_cap REAL,
        pe_ratio REAL,
        fifty_two_week_high REAL,
        fifty_two_week_low REAL,
        current_price REAL,
        last_updated TIMESTAMP
    )
    """)
    
    # 2. Daily Price History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        date TEXT NOT NULL,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        UNIQUE(symbol, date),
        FOREIGN KEY(symbol) REFERENCES stocks(symbol)
    )
    """)
    
    # 3. Technical Indicators Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technical_indicators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        date TEXT NOT NULL,
        sma_20 REAL,
        sma_50 REAL,
        ema_20 REAL,
        rsi_14 REAL,
        macd REAL,
        macd_signal REAL,
        UNIQUE(symbol, date),
        FOREIGN KEY(symbol) REFERENCES stocks(symbol)
    )
    """)
    
    # 4. Machine Learning & ARIMA Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        model_type TEXT NOT NULL,
        prediction_date TEXT NOT NULL,
        predicted_trend TEXT,
        confidence_pct REAL,
        accuracy_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(symbol) REFERENCES stocks(symbol)
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {DB_PATH}")

def save_stock_metadata(info: Dict[str, Any]):
    """Insert or update stock metadata."""
    if not info or not info.get("symbol"):
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO stocks (symbol, company_name, sector, market_cap, pe_ratio, fifty_two_week_high, fifty_two_week_low, current_price, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(symbol) DO UPDATE SET
        company_name = excluded.company_name,
        sector = excluded.sector,
        market_cap = excluded.market_cap,
        pe_ratio = excluded.pe_ratio,
        fifty_two_week_high = excluded.fifty_two_week_high,
        fifty_two_week_low = excluded.fifty_two_week_low,
        current_price = excluded.current_price,
        last_updated = excluded.last_updated
    """, (
        info.get("symbol", "").upper(),
        info.get("companyName"),
        info.get("sector"),
        info.get("marketCap"),
        info.get("peRatio"),
        info.get("fiftyTwoWeekHigh"),
        info.get("fiftyTwoWeekLow"),
        info.get("regularMarketPrice"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def save_price_history_df(symbol: str, df: pd.DataFrame):
    """Insert daily OHLCV rows from DataFrame into SQLite table."""
    if df is None or df.empty:
        return
    conn = get_connection()
    cursor = conn.cursor()
    symbol = symbol.upper()

    df_copy = df.copy()
    if df_copy.index.name in ["Date", "Datetime"] or isinstance(df_copy.index, pd.DatetimeIndex):
        df_copy = df_copy.reset_index()
        
    date_col = "Date" if "Date" in df_copy.columns else df_copy.columns[0]
    
    for _, row in df_copy.iterrows():
        try:
            d_val = pd.to_datetime(row[date_col]).strftime("%Y-%m-%d")
            cursor.execute("""
            INSERT INTO price_history (symbol, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(symbol, date) DO UPDATE SET
                open = excluded.open,
                high = excluded.high,
                low = excluded.low,
                close = excluded.close,
                volume = excluded.volume
            """, (
                symbol,
                d_val,
                float(row.get("Open", 0.0)),
                float(row.get("High", 0.0)),
                float(row.get("Low", 0.0)),
                float(row.get("Close", 0.0)),
                int(row.get("Volume", 0))
            ))
        except Exception:
            continue
            
    conn.commit()
    conn.close()

def save_prediction_record(symbol: str, model_type: str, prediction_date: str, trend: str, confidence: float, accuracy: float):
    """Logs a model prediction into SQLite database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO model_predictions (symbol, model_type, prediction_date, predicted_trend, confidence_pct, accuracy_score, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        symbol.upper(),
        model_type,
        prediction_date,
        trend,
        confidence,
        accuracy,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def get_database_summary() -> Dict[str, Any]:
    """Returns row counts and metadata for each database table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM stocks")
    stocks_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM price_history")
    prices_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM model_predictions")
    preds_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT symbol, company_name, current_price, last_updated FROM stocks")
    stocks_list = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {
        "database_file": os.path.basename(DB_PATH),
        "database_path": DB_PATH,
        "stocks_tracked": stocks_count,
        "total_price_records": prices_count,
        "total_predictions_logged": preds_count,
        "stocks": stocks_list
    }
