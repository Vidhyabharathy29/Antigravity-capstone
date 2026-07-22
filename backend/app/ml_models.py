import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import Dict, Any, Tuple, List

from .indicators import add_all_indicators

def build_features(df: pd.DataFrame, lags: int = 5) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """
    Build features for predicting stock trend.
    Target is 1 if tomorrow's Close > today's Close, else 0.
    
    Features constructed:
    - Returns (lagged)
    - Volume percent change (lagged)
    - SMA/EMA ratios
    - RSI
    - MACD indicators
    - Rolling volatility
    """
    # Make sure we have indicators
    df_ind = add_all_indicators(df)
    
    # Calculate daily returns
    df_ind["Return"] = df_ind["Close"].pct_change()
    df_ind["Vol_Change"] = df_ind["Volume"].pct_change()
    df_ind["Volatility_10"] = df_ind["Return"].rolling(window=10).std()
    
    # Ratios
    df_ind["SMA20_Ratio"] = df_ind["SMA_20"] / df_ind["Close"]
    df_ind["SMA50_Ratio"] = df_ind["SMA_50"] / df_ind["Close"]
    df_ind["EMA20_Ratio"] = df_ind["EMA_20"] / df_ind["Close"]
    df_ind["RSI_Norm"] = df_ind["RSI_14"] / 100.0
    df_ind["MACD_Ratio"] = df_ind["MACD"] / df_ind["Close"]
    
    feature_cols = [
        "SMA20_Ratio", "SMA50_Ratio", "EMA20_Ratio", "RSI_Norm", "MACD_Ratio", "Volatility_10"
    ]
    
    # Add lags of returns and volume change
    for lag in range(1, lags + 1):
        df_ind[f"Return_Lag_{lag}"] = df_ind["Return"].shift(lag)
        df_ind[f"Vol_Lag_{lag}"] = df_ind["Vol_Change"].shift(lag)
        feature_cols.extend([f"Return_Lag_{lag}", f"Vol_Lag_{lag}"])
        
    # Define Target: 1 if tomorrow's Close > today's Close, 0 otherwise
    df_ind["Target"] = (df_ind["Close"].shift(-1) > df_ind["Close"]).astype(int)
    
    # Clean data (drop first rows with NaNs due to rolling/lags and the very last row which doesn't have a tomorrow target)
    df_clean = df_ind.dropna().copy()
    
    X = df_clean[feature_cols]
    y = df_clean["Target"]
    
    return X, y, feature_cols

def train_and_evaluate_ml(
    df: pd.DataFrame,
    model_type: str = "rf",
    n_estimators: int = 100,
    max_depth: int = 6,
    lags: int = 5,
    test_size: float = 0.2
) -> Dict[str, Any]:
    """
    Run the machine learning training pipeline.
    - Creates features & targets
    - Splits sequentially (time-series split)
    - Fits a Random Forest or Gradient Boosting Classifier
    - Computes metrics on test set
    - Outputs feature importances
    - Predicts tomorrow's price direction based on the most recent data
    """
    if len(df) < 50:
        return {
            "success": False,
            "error": "Dataset is too small for machine learning training. Need at least 50 trading days."
        }
        
    try:
        # Build features
        X, y, feature_cols = build_features(df, lags=lags)
        
        if len(X) < 20:
            return {
                "success": False,
                "error": "Insufficient samples after feature engineering."
            }
            
        # Chronological Train-Test Split (Avoiding lookahead bias)
        split_idx = int(len(X) * (1 - test_size))
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # Instantiate model
        if model_type == "gb":
            model = GradientBoostingClassifier(
                n_estimators=n_estimators, 
                max_depth=max_depth, 
                random_state=42
            )
        else:
            model = RandomForestClassifier(
                n_estimators=n_estimators, 
                max_depth=max_depth, 
                random_state=42,
                n_jobs=-1
            )
            
        # Train model
        model.fit(X_train, y_train)
        
        # Predict on test set
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] # Probability of UP
        
        # Calculate evaluation metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # Feature importances
        importances = model.feature_importances_
        importance_list = [
            {"feature": col, "importance": float(imp)}
            for col, imp in zip(feature_cols, importances)
        ]
        importance_list = sorted(importance_list, key=lambda x: x["importance"], reverse=True)
        
        # Now predict TOMORROW's trend (using the absolute last row of our stock data)
        # Note: the target shift(-1) was missing for the last row, but features are fully populated.
        # Let's extract features for the actual last day in the original dataset
        df_ind_full = add_all_indicators(df)
        df_ind_full["Return"] = df_ind_full["Close"].pct_change()
        df_ind_full["Vol_Change"] = df_ind_full["Volume"].pct_change()
        df_ind_full["Volatility_10"] = df_ind_full["Return"].rolling(window=10).std()
        df_ind_full["SMA20_Ratio"] = df_ind_full["SMA_20"] / df_ind_full["Close"]
        df_ind_full["SMA50_Ratio"] = df_ind_full["SMA_50"] / df_ind_full["Close"]
        df_ind_full["EMA20_Ratio"] = df_ind_full["EMA_20"] / df_ind_full["Close"]
        df_ind_full["RSI_Norm"] = df_ind_full["RSI_14"] / 100.0
        df_ind_full["MACD_Ratio"] = df_ind_full["MACD"] / df_ind_full["Close"]
        
        for lag in range(1, lags + 1):
            df_ind_full[f"Return_Lag_{lag}"] = df_ind_full["Return"].shift(lag)
            df_ind_full[f"Vol_Lag_{lag}"] = df_ind_full["Vol_Change"].shift(lag)
            
        latest_features = df_ind_full[feature_cols].iloc[[-1]]
        
        # Check if there are any NaNs in the latest features
        if latest_features.isnull().values.any():
            # Backfill to ensure we can run a prediction
            latest_features = latest_features.bfill().ffill().fillna(0)
            
        tomorrow_prob = float(model.predict_proba(latest_features)[0, 1])
        tomorrow_prediction = int(model.predict(latest_features)[0])
        
        return {
            "success": True,
            "metrics": {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1)
            },
            "feature_importances": importance_list,
            "tomorrow": {
                "prediction": "UP" if tomorrow_prediction == 1 else "DOWN",
                "probability": tomorrow_prob,
                "date": (pd.to_datetime(df.index[-1]) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
            }
        }
        
    except Exception as e:
        print(f"Error training ML model: {e}")
        return {
            "success": False,
            "error": str(e)
        }
