import React, { useState } from 'react';
import { TrendingUp, Activity, Cpu, Search, CheckCircle2, AlertCircle } from 'lucide-react';

const PRESET_TICKERS = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOGL', 'AMZN'];

export default function Navbar({ currentTicker, setTicker, activeTab, setActiveTab, apiStatus }) {
  const [searchInput, setSearchInput] = useState('');

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      setTicker(searchInput.trim().toUpperCase());
      setSearchInput('');
    }
  };

  return (
    <header className="glass-panel" style={{ borderRadius: '0 0 var(--radius-md) var(--radius-md)', padding: '1rem 2rem', marginBottom: '2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        
        {/* Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            background: 'var(--gradient-primary)',
            padding: '0.5rem',
            borderRadius: 'var(--radius-sm)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-glow)'
          }}>
            <TrendingUp size={24} color="#fff" />
          </div>
          <div>
            <h1 style={{ fontSize: '1.25rem', lineHeight: 1.2 }} className="gradient-text">
              StockTrend AI
            </h1>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'block' }}>
              ML & Time Series Analytics Platform
            </span>
          </div>
        </div>

        {/* Ticker Search & Presets */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '0.5rem' }}>
            <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
              <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '0.75rem' }} />
              <input
                type="text"
                className="input-field"
                placeholder="Search symbol (e.g. NVDA)..."
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                style={{ paddingLeft: '2.25rem', width: '220rem', maxWidth: '220px' }}
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Query
            </button>
          </form>

          {/* Quick Presets */}
          <div style={{ display: 'flex', gap: '0.35rem', alignItems: 'center' }}>
            {PRESET_TICKERS.map((t) => (
              <button
                key={t}
                onClick={() => setTicker(t)}
                className={`btn ${currentTicker === t ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Navigation Tabs & Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <nav style={{ display: 'flex', background: 'rgba(0,0,0,0.3)', padding: '0.25rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
            <button
              onClick={() => setActiveTab('dashboard')}
              style={{
                background: activeTab === 'dashboard' ? 'var(--accent-primary)' : 'transparent',
                color: activeTab === 'dashboard' ? '#fff' : 'var(--text-secondary)',
                border: 'none',
                padding: '0.5rem 1rem',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                transition: 'all var(--transition-fast)'
              }}
            >
              <TrendingUp size={16} /> Market Overview
            </button>
            
            <button
              onClick={() => setActiveTab('ts')}
              style={{
                background: activeTab === 'ts' ? 'var(--accent-primary)' : 'transparent',
                color: activeTab === 'ts' ? '#fff' : 'var(--text-secondary)',
                border: 'none',
                padding: '0.5rem 1rem',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                transition: 'all var(--transition-fast)'
              }}
            >
              <Activity size={16} /> ARIMA Forecast
            </button>

            <button
              onClick={() => setActiveTab('ml')}
              style={{
                background: activeTab === 'ml' ? 'var(--accent-primary)' : 'transparent',
                color: activeTab === 'ml' ? '#fff' : 'var(--text-secondary)',
                border: 'none',
                padding: '0.5rem 1rem',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                transition: 'all var(--transition-fast)'
              }}
            >
              <Cpu size={16} /> ML Predictor
            </button>
          </nav>

          {/* API Status Badge */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', color: apiStatus ? 'var(--accent-success)' : 'var(--accent-danger)' }}>
            {apiStatus ? <CheckCircle2 size={14} /> : <AlertCircle size={14} />}
            <span>{apiStatus ? 'API Connected' : 'API Offline'}</span>
          </div>
        </div>

      </div>
    </header>
  );
}
