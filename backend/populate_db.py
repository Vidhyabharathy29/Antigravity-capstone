import os
import glob
import pandas as pd
from app.database import init_db, save_price_history_df, save_stock_metadata, save_prediction_record, get_database_summary

def populate():
    print("Initializing SQLite Database...")
    init_db()
    
    # 1. Seed stock metadata
    seed_stocks = [
        {"symbol": "AAPL", "companyName": "Apple Inc.", "sector": "Technology", "marketCap": 5068850987008, "peRatio": 39.83, "fiftyTwoWeekHigh": 351.73, "fiftyTwoWeekLow": 243.42, "regularMarketPrice": 347.32},
        {"symbol": "NVDA", "companyName": "NVIDIA Corporation", "sector": "Technology", "marketCap": 3200000000000, "peRatio": 65.20, "fiftyTwoWeekHigh": 140.76, "fiftyTwoWeekLow": 45.11, "regularMarketPrice": 138.25},
        {"symbol": "TSLA", "companyName": "Tesla, Inc.", "sector": "Consumer Cyclical", "marketCap": 780000000000, "peRatio": 72.15, "fiftyTwoWeekHigh": 271.00, "fiftyTwoWeekLow": 138.80, "regularMarketPrice": 220.50},
        {"symbol": "MSFT", "companyName": "Microsoft Corporation", "sector": "Technology", "marketCap": 3150000000000, "peRatio": 36.40, "fiftyTwoWeekHigh": 468.35, "fiftyTwoWeekLow": 366.50, "regularMarketPrice": 448.10},
        {"symbol": "GOOGL", "companyName": "Alphabet Inc.", "sector": "Communication Services", "marketCap": 2100000000000, "peRatio": 24.10, "fiftyTwoWeekHigh": 191.75, "fiftyTwoWeekLow": 129.40, "regularMarketPrice": 178.60},
        {"symbol": "AMZN", "companyName": "Amazon.com, Inc.", "sector": "Consumer Cyclical", "marketCap": 1950000000000, "peRatio": 42.80, "fiftyTwoWeekHigh": 201.20, "fiftyTwoWeekLow": 118.35, "regularMarketPrice": 186.40}
    ]
    
    for s in seed_stocks:
        save_stock_metadata(s)
    print(f"Loaded {len(seed_stocks)} company profiles into 'stocks' table.")
    
    # 2. Ingest all cached CSVs into price_history
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
    csv_files = glob.glob(os.path.join(cache_dir, "*_2y.csv"))
    
    total_records = 0
    for csv_file in csv_files:
        base = os.path.basename(csv_file)
        ticker = base.split("_")[0]
        try:
            df = pd.read_csv(csv_file, index_col=0, parse_dates=True)
            save_price_history_df(ticker, df)
            print(f"  -> Ingested {len(df)} rows for {ticker} from {base}")
            total_records += len(df)
        except Exception as e:
            print(f"  Error reading {base}: {e}")
            
    # 3. Seed sample model predictions
    save_prediction_record("AAPL", "Random Forest", "Next Trading Day", "UP", 68.5, 0.74)
    save_prediction_record("NVDA", "Gradient Boosting", "Next Trading Day", "UP", 72.1, 0.78)
    save_prediction_record("TSLA", "Random Forest", "Next Trading Day", "DOWN", 58.2, 0.65)
    
    summary = get_database_summary()
    print("\n--- DATABASE SUMMARY ---")
    print(f"Database File: {summary['database_file']}")
    print(f"Stocks Tracked: {summary['stocks_tracked']}")
    print(f"Total Price History Records: {summary['total_price_records']}")
    print(f"Predictions Logged: {summary['total_predictions_logged']}")
    print("Database population completed successfully!")

if __name__ == "__main__":
    populate()
