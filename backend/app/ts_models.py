import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from typing import Dict, Any, Tuple, List

def evaluate_arima_performance(series: pd.Series, p: int, d: int, q: int) -> Dict[str, Any]:
    """
    Perform a train-test split (80% train, 20% test) on the historical data
    and evaluate the ARIMA model performance on the test set.
    """
    try:
        n = len(series)
        if n < 30:
            return {"error": "Insufficient data to train ARIMA. Need at least 30 observations."}
            
        split_idx = int(n * 0.8)
        train = series.iloc[:split_idx]
        test = series.iloc[split_idx:]
        
        # Fit model on training data
        # enforce_stationarity=False and enforce_invertibility=False help avoid convergence issues on raw financial data
        model = ARIMA(train, order=(p, d, q), enforce_stationarity=False, enforce_invertibility=False)
        model_fit = model.fit()
        
        # Forecast test set length
        forecast_res = model_fit.forecast(steps=len(test))
        
        # Calculate metrics
        mae = np.mean(np.abs(test.values - forecast_res.values))
        rmse = np.sqrt(np.mean((test.values - forecast_res.values) ** 2))
        mape = np.mean(np.abs((test.values - forecast_res.values) / test.values)) * 100
        
        return {
            "mae": float(mae),
            "rmse": float(rmse),
            "mape": float(mape),
            "aic": float(model_fit.aic),
            "bic": float(model_fit.bic)
        }
    except Exception as e:
        print(f"Error evaluating ARIMA performance: {e}")
        return {"error": str(e)}

def fit_and_forecast_arima(
    series: pd.Series, 
    p: int = 1, 
    d: int = 1, 
    q: int = 1, 
    forecast_steps: int = 30
) -> Dict[str, Any]:
    """
    Fit ARIMA model on all historical data and forecast the next N steps.
    Returns:
    - dates: list of future dates (as strings)
    - predictions: list of predicted prices
    - lower_bound: list of 95% confidence lower bounds
    - upper_bound: list of 95% confidence upper bounds
    - metrics: dictionary containing evaluation metrics (MAE, RMSE, MAPE, AIC, BIC)
    """
    try:
        n = len(series)
        if n < 30:
            raise ValueError("Insufficient data to fit ARIMA. Need at least 30 observations.")
            
        # 1. Evaluate on split
        metrics = evaluate_arima_performance(series, p, d, q)
        
        # 2. Fit on complete historical dataset
        model = ARIMA(series, order=(p, d, q), enforce_stationarity=False, enforce_invertibility=False)
        model_fit = model.fit()
        
        # 3. Forecast future steps
        forecast_result = model_fit.get_forecast(steps=forecast_steps)
        forecast_mean = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int(alpha=0.05) # 95% CI
        
        # Generate future dates
        last_date = pd.to_datetime(series.index[-1])
        # Use business days to match stock market schedule
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps, freq="B")
        
        # Extract lower and upper bounds (column names depend on pandas series name)
        lower_col = conf_int.columns[0]
        upper_col = conf_int.columns[1]
        
        lower_bounds = conf_int[lower_col].values
        upper_bounds = conf_int[upper_col].values
        
        # Handle cases where prices forecast below 0 (clip to 0.01)
        predictions = np.clip(forecast_mean.values, 0.01, None)
        lower_bounds = np.clip(lower_bounds, 0.01, None)
        upper_bounds = np.clip(upper_bounds, 0.01, None)
        
        return {
            "dates": [d.strftime("%Y-%m-%d") for d in future_dates],
            "predictions": [float(val) for val in predictions],
            "lower_bound": [float(val) for val in lower_bounds],
            "upper_bound": [float(val) for val in upper_bounds],
            "metrics": metrics,
            "success": True
        }
        
    except Exception as e:
        print(f"Error fitting ARIMA: {e}")
        # Fallback to simple drift or naive forecasting if fit completely fails
        try:
            last_val = series.iloc[-1]
            last_date = pd.to_datetime(series.index[-1])
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps, freq="B")
            
            # Simple naive constant forecast with increasing standard error bounds
            predictions = np.full(forecast_steps, last_val)
            std_err = np.std(series.pct_change().dropna()) * last_val
            lower_bounds = [float(max(0.01, last_val - 1.96 * std_err * np.sqrt(i + 1))) for i in range(forecast_steps)]
            upper_bounds = [float(last_val + 1.96 * std_err * np.sqrt(i + 1)) for i in range(forecast_steps)]
            
            return {
                "dates": [d.strftime("%Y-%m-%d") for d in future_dates],
                "predictions": [float(val) for val in predictions],
                "lower_bound": lower_bounds,
                "upper_bound": upper_bounds,
                "metrics": {"error": f"ARIMA fit failed ({str(e)}). Displaying baseline naive drift."},
                "success": False
            }
        except Exception as fallback_err:
            return {
                "success": False,
                "error": f"ARIMA and Fallback both failed. Details: {str(fallback_err)}"
            }
