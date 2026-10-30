import React, { useState, useEffect } from 'react';
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell
} from 'recharts';
import { Cpu, TrendingUp, TrendingDown, Target, Award, Sliders, Zap } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function MLPrediction({ ticker }) {
  const [modelType, setModelType] = useState('rf');
  const [nEstimators, setNEstimators] = useState(100);
  const [maxDepth, setMaxDepth] = useState(6);
  const [lags, setLags] = useState(5);
  const [testSize, setTestSize] = useState(0.2);

  const [mlData, setMlData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const trainModel = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/train_ml`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticker,
          model_type: modelType,
          n_estimators: nEstimators,
          max_depth: maxDepth,
          lags,
          test_size: testSize
        })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to train ML model.');
      }

      const data = await response.json();
      setMlData(data);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error training Machine Learning model.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    trainModel();
  }, [ticker]);

  const tomorrow = mlData?.tomorrow;
  const metrics = mlData?.metrics;
  const importances = mlData?.feature_importances ? mlData.feature_importances.slice(0, 8) : [];

  const isUp = tomorrow?.prediction === 'UP';
  const confidencePercent = tomorrow?.probability
    ? (isUp ? tomorrow.probability * 100 : (1 - tomorrow.probability) * 100).toFixed(1)
    : '0';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }} className="animate-fade-in">
      
      {/* Top Header & Hyperparameter Tuner */}
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
          <div>
            <h2 style={{ fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Cpu color="var(--accent-primary)" /> Machine Learning Direction Predictor
            </h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
              Feature-engineered supervised classifier trained on technical momentum, volatility, and lagged returns to predict next-day price movement.
            </p>
          </div>

          <button onClick={trainModel} className="btn btn-primary" disabled={loading}>
            {loading ? 'Training Ensemble Model...' : 'Retrain Model'}
          </button>
        </div>

        {/* Hyperparameter Controls Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '1rem', background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              Algorithm
            </label>
            <select
              className="input-field"
              value={modelType}
              onChange={(e) => setModelType(e.target.value)}
              style={{ width: '100%' }}
            >
              <option value="rf">Random Forest</option>
              <option value="gb">Gradient Boosting</option>
            </select>
          </div>

          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              Trees (n_estimators)
            </label>
            <input
              type="number"
              min="10"
              max="300"
              step="10"
              className="input-field"
              value={nEstimators}
              onChange={(e) => setNEstimators(parseInt(e.target.value) || 100)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              Max Tree Depth
            </label>
            <input
              type="number"
              min="2"
              max="15"
              className="input-field"
              value={maxDepth}
              onChange={(e) => setMaxDepth(parseInt(e.target.value) || 6)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              Return Lags
            </label>
            <input
              type="number"
              min="1"
              max="10"
              className="input-field"
              value={lags}
              onChange={(e) => setLags(parseInt(e.target.value) || 5)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.25rem' }}>
              Test Split
            </label>
            <select
              className="input-field"
              value={testSize}
              onChange={(e) => setTestSize(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            >
              <option value={0.15}>15% Test</option>
              <option value={0.2}>20% Test</option>
              <option value={0.3}>30% Test</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Prediction & Metrics Display */}
      {loading ? (
        <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
          <div>Training Machine Learning classifier on {ticker} feature matrix...</div>
        </div>
      ) : error ? (
        <div className="glass-panel" style={{ padding: '2rem', color: 'var(--accent-danger)', textAlign: 'center' }}>
          {error}
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
          
          {/* Tomorrow's Trend Forecast Card */}
          <div className="glass-panel glass-panel-glow" style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
                  Next Trading Day Forecast
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Target Date: {tomorrow?.date}</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.25rem' }}>
                <div style={{
                  background: isUp ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)',
                  border: isUp ? '1px solid var(--accent-success)' : '1px solid var(--accent-danger)',
                  padding: '1rem',
                  borderRadius: 'var(--radius-md)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  {isUp ? <TrendingUp size={36} color="var(--accent-success)" /> : <TrendingDown size={36} color="var(--accent-danger)" />}
                </div>

                <div>
                  <div style={{ fontSize: '2.25rem', fontWeight: '800', color: isUp ? 'var(--accent-success)' : 'var(--accent-danger)', lineHeight: 1.1 }}>
                    {tomorrow?.prediction || 'N/A'}
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    Expected Trend Direction
                  </div>
                </div>
              </div>
            </div>

            {/* Probability Progress Bar */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.4rem' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Model Directional Confidence</span>
                <span style={{ fontWeight: '700', color: 'var(--text-primary)' }}>{confidencePercent}%</span>
              </div>
              <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.08)', borderRadius: '4px', overflow: 'hidden' }}>
                <div
                  style={{
                    width: `${confidencePercent}%`,
                    height: '100%',
                    background: isUp ? 'var(--accent-success)' : 'var(--accent-danger)',
                    borderRadius: '4px',
                    transition: 'width 0.6s ease'
                  }}
                />
              </div>
            </div>

          </div>

          {/* Test Set Accuracy & Metrics Grid */}
          <div className="glass-panel" style={{ padding: '1.75rem' }}>
            <h3 style={{ fontSize: '1rem', marginBottom: '1.25rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Award size={18} color="var(--accent-warning)" /> Test Set Out-of-Sample Performance
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Accuracy</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                  {metrics ? `${(metrics.accuracy * 100).toFixed(1)}%` : 'N/A'}
                </div>
              </div>

              <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Precision</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-secondary)' }}>
                  {metrics ? `${(metrics.precision * 100).toFixed(1)}%` : 'N/A'}
                </div>
              </div>

              <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Recall</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-primary)' }}>
                  {metrics ? `${(metrics.recall * 100).toFixed(1)}%` : 'N/A'}
                </div>
              </div>

              <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>F1-Score</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-success)' }}>
                  {metrics ? `${(metrics.f1_score * 100).toFixed(1)}%` : 'N/A'}
                </div>
              </div>
            </div>
          </div>

        </div>
      )}

      {/* Feature Importances Bar Chart */}
      {importances.length > 0 && !loading && (
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', marginBottom: '1rem', color: 'var(--text-secondary)' }}>
            Key Feature Importances (What Drove the Model's Decision)
          </h3>

          <div style={{ height: '260px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={importances} margin={{ top: 5, right: 30, left: 70, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis type="number" stroke="#6b7280" tick={{ fontSize: 10 }} />
                <YAxis dataKey="feature" type="category" stroke="#6b7280" tick={{ fontSize: 11 }} width={90} />
                <Tooltip
                  contentStyle={{ background: '#111827', borderColor: '#374151', borderRadius: '8px' }}
                  formatter={(val) => [(val * 100).toFixed(2) + '%', 'Importance']}
                />
                <Bar dataKey="importance" fill="#6366f1" radius={[0, 4, 4, 0]}>
                  {importances.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={index === 0 ? '#6366f1' : index === 1 ? '#06b6d4' : '#818cf8'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

    </div>
  );
}
