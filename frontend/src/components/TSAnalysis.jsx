import React, { useState, useEffect } from 'react';
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, Area, ComposedChart
} from 'recharts';
import { Activity, Sliders, AlertCircle, CheckCircle, HelpCircle } from 'lucide-react';

export default function TSAnalysis({ ticker, historyData }) {
  const [p, setP] = useState(1);
  const [d, setD] = useState(1);
  const [q, setQ] = useState(1);
  const [steps, setSteps] = useState(30);

  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runForecast = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `http://localhost:8000/api/forecast?ticker=${ticker}&p=${p}&d=${d}&q=${q}&steps=${steps}`
      );
      if (!response.ok) {
        throw new Error(`Failed to fetch forecast: ${response.statusText}`);
      }
      const data = await response.json();
      setForecastData(data);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error running ARIMA forecast.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runForecast();
  }, [ticker]);

  // Combine historical data with forecast data for continuous line chart rendering
  const getCombinedChartData = () => {
    if (!historyData || historyData.length === 0) return [];
    
    // Take recent historical slice (e.g. last 60 days) to keep chart legible
    const recentHist = historyData.slice(-60).map(item => ({
      Date: item.Date,
      Historical: item.Close,
      Forecast: null,
      Lower: null,
      Upper: null
    }));

    if (!forecastData || !forecastData.dates) return recentHist;

    // Last historical point acts as anchor for forecast
    const lastHist = recentHist[recentHist.length - 1];

    const forecastPoints = forecastData.dates.map((dateStr, idx) => ({
      Date: dateStr,
      Historical: idx === 0 ? lastHist.Historical : null,
      Forecast: forecastData.predictions[idx],
      Lower: forecastData.lower_bound[idx],
      Upper: forecastData.upper_bound[idx]
    }));

    // Connect the last historical point with the first forecast point
    forecastPoints[0].Forecast = lastHist.Historical;
    forecastPoints[0].Lower = lastHist.Historical;
    forecastPoints[0].Upper = lastHist.Historical;

    return [...recentHist, ...forecastPoints];
  };

  const combinedData = getCombinedChartData();
  const metrics = forecastData?.metrics;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }} className="animate-fade-in">
      
      {/* Header & Controls Panel */}
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
          <div>
            <h2 style={{ fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Activity color="var(--accent-secondary)" /> ARIMA Time Series Forecasting
            </h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
              Autoregressive Integrated Moving Average model for stock price trend projection with 95% confidence bounds.
            </p>
          </div>

          <button onClick={runForecast} className="btn btn-primary" disabled={loading}>
            {loading ? 'Fitting ARIMA Model...' : 'Re-Run Forecast'}
          </button>
        </div>

        {/* Hyperparameter Inputs */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '1rem', background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              p (AR Lag Order)
            </label>
            <input
              type="number"
              min="0"
              max="10"
              className="input-field"
              value={p}
              onChange={(e) => setP(parseInt(e.target.value) || 0)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              d (Differencing Degree)
            </label>
            <input
              type="number"
              min="0"
              max="2"
              className="input-field"
              value={d}
              onChange={(e) => setD(parseInt(e.target.value) || 0)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              q (MA Window Size)
            </label>
            <input
              type="number"
              min="0"
              max="10"
              className="input-field"
              value={q}
              onChange={(e) => setQ(parseInt(e.target.value) || 0)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              Forecast Horizon (Days)
            </label>
            <input
              type="number"
              min="5"
              max="90"
              className="input-field"
              value={steps}
              onChange={(e) => setSteps(parseInt(e.target.value) || 30)}
              style={{ width: '100%' }}
            />
          </div>
        </div>
      </div>

      {/* Model Performance Metrics Cards */}
      {metrics && !metrics.error && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
          <div className="glass-panel" style={{ padding: '1rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Mean Absolute Error (MAE)</div>
            <div style={{ fontSize: '1.35rem', fontWeight: '700', color: 'var(--accent-secondary)' }}>${metrics.mae.toFixed(2)}</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Average deviation on test split</div>
          </div>

          <div className="glass-panel" style={{ padding: '1rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Root Mean Squared Error (RMSE)</div>
            <div style={{ fontSize: '1.35rem', fontWeight: '700', color: 'var(--accent-primary)' }}>${metrics.rmse.toFixed(2)}</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Penalizes larger prediction errors</div>
          </div>

          <div className="glass-panel" style={{ padding: '1rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>MAPE (Percentage Error)</div>
            <div style={{ fontSize: '1.35rem', fontWeight: '700', color: 'var(--accent-success)' }}>{metrics.mape.toFixed(2)}%</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Relative forecast accuracy</div>
          </div>

          <div className="glass-panel" style={{ padding: '1rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Akaike Info Criterion (AIC)</div>
            <div style={{ fontSize: '1.35rem', fontWeight: '700', color: 'var(--accent-warning)' }}>{metrics.aic.toFixed(1)}</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Lower score indicates better fit</div>
          </div>
        </div>
      )}

      {/* Main Forecast Visualizer */}
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '1rem', color: 'var(--text-secondary)' }}>
          {ticker} - Historical vs. ARIMA ({p},{d},{q}) Projected Future Trajectory
        </h3>

        {loading ? (
          <div style={{ height: '380px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
            Fitting ARIMA Model to price series...
          </div>
        ) : error ? (
          <div style={{ height: '200px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-danger)' }}>
            <AlertCircle size={32} style={{ marginBottom: '0.5rem' }} />
            {error}
          </div>
        ) : (
          <div style={{ height: '400px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={combinedData} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="Date" stroke="#6b7280" tick={{ fontSize: 11 }} />
                <YAxis domain={['auto', 'auto']} stroke="#6b7280" tick={{ fontSize: 11 }} tickFormatter={(v) => `$${v}`} />
                <Tooltip
                  contentStyle={{ background: '#111827', borderColor: '#374151', borderRadius: '8px', color: '#fff' }}
                  formatter={(val, name) => [typeof val === 'number' ? `$${val.toFixed(2)}` : val, name]}
                />
                <Legend />
                
                {/* Confidence Interval Band */}
                <Area type="monotone" dataKey="Upper" stroke="none" fill="rgba(6, 182, 212, 0.15)" name="95% Confidence Upper Bound" />
                <Area type="monotone" dataKey="Lower" stroke="none" fill="rgba(6, 182, 212, 0.05)" name="95% Confidence Lower Bound" />

                {/* Historical Price */}
                <Line type="monotone" dataKey="Historical" stroke="#6366f1" strokeWidth={2.5} dot={false} name="Historical Close" />

                {/* ARIMA Forecast */}
                <Line type="monotone" dataKey="Forecast" stroke="#06b6d4" strokeWidth={2.5} strokeDasharray="4 4" dot={{ r: 3, fill: '#06b6d4' }} name="ARIMA Forecast" />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

    </div>
  );
}
