import React, { useState } from 'react';
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, BarChart, Bar, ReferenceLine
} from 'recharts';
import { DollarSign, BarChart2, Zap, ArrowUpRight, ArrowDownRight, Layers } from 'lucide-react';

export default function Dashboard({ stockInfo, historyData, period, setPeriod, loading }) {
  const [activeIndicators, setActiveIndicators] = useState({
    sma20: true,
    sma50: false,
    ema20: true,
    rsi: true,
    macd: true
  });

  const toggleIndicator = (key) => {
    setActiveIndicators(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const formatCurrency = (num) => {
    if (num === null || num === undefined || isNaN(num)) return 'N/A';
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: stockInfo?.currency || 'USD' }).format(num);
  };

  const formatCompactNumber = (num) => {
    if (!num) return 'N/A';
    if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    return num.toLocaleString();
  };

  // Calculate recent performance percentage change
  const priceChange = historyData.length > 1
    ? historyData[historyData.length - 1].Close - historyData[0].Close
    : 0;
  const priceChangePercent = historyData.length > 1
    ? (priceChange / historyData[0].Close) * 100
    : 0;
  const isPositive = priceChange >= 0;

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0', color: 'var(--text-secondary)' }}>
        <div style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Loading Stock Market Analytics...</div>
        <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Fetching historical price data & computing indicators...</div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }} className="animate-fade-in">
      
      {/* Top Banner: Key Stats Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        
        {/* Current Price */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
            <span>{stockInfo?.companyName || stockInfo?.symbol}</span>
            <DollarSign size={18} color="var(--accent-primary)" />
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: '800', marginBottom: '0.25rem' }}>
            {formatCurrency(stockInfo?.regularMarketPrice || (historyData.length ? historyData[historyData.length - 1].Close : 0))}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', fontSize: '0.85rem', color: isPositive ? 'var(--accent-success)' : 'var(--accent-danger)' }}>
            {isPositive ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
            <span style={{ fontWeight: 600 }}>{isPositive ? '+' : ''}{priceChange.toFixed(2)} ({priceChangePercent.toFixed(2)}%)</span>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginLeft: '0.25rem' }}>over period</span>
          </div>
        </div>

        {/* Market Cap */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
            <span>Market Capitalization</span>
            <BarChart2 size={18} color="var(--accent-secondary)" />
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: '800', marginBottom: '0.25rem' }}>
            {formatCompactNumber(stockInfo?.marketCap)}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            Sector: <span style={{ color: 'var(--text-primary)' }}>{stockInfo?.sector || 'N/A'}</span>
          </div>
        </div>

        {/* 52-Week Range */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
            <span>52-Week Range</span>
            <Zap size={18} color="var(--accent-warning)" />
          </div>
          <div style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '0.4rem' }}>
            {formatCurrency(stockInfo?.fiftyTwoWeekLow)} - {formatCurrency(stockInfo?.fiftyTwoWeekHigh)}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            P/E Ratio: <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{stockInfo?.peRatio ? stockInfo.peRatio.toFixed(2) : 'N/A'}</span>
          </div>
        </div>

      </div>

      {/* Main Chart Section */}
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        
        {/* Controls Bar: Timeframe & Indicators */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
          
          {/* Timeframes */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Timeframe:</span>
            {['1mo', '3mo', '6mo', '1y', '2y', '5y'].map((p) => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={`btn ${period === p ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
              >
                {p.toUpperCase()}
              </button>
            ))}
          </div>

          {/* Indicator Toggles */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
              <Layers size={14} /> Overlays:
            </span>
            
            <button
              onClick={() => toggleIndicator('sma20')}
              style={{
                background: activeIndicators.sma20 ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255,255,255,0.05)',
                color: activeIndicators.sma20 ? '#818cf8' : 'var(--text-muted)',
                border: activeIndicators.sma20 ? '1px solid #6366f1' : '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.3rem 0.6rem',
                fontSize: '0.75rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              SMA 20
            </button>

            <button
              onClick={() => toggleIndicator('sma50')}
              style={{
                background: activeIndicators.sma50 ? 'rgba(245, 158, 11, 0.2)' : 'rgba(255,255,255,0.05)',
                color: activeIndicators.sma50 ? '#fbbf24' : 'var(--text-muted)',
                border: activeIndicators.sma50 ? '1px solid #f59e0b' : '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.3rem 0.6rem',
                fontSize: '0.75rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              SMA 50
            </button>

            <button
              onClick={() => toggleIndicator('ema20')}
              style={{
                background: activeIndicators.ema20 ? 'rgba(6, 182, 212, 0.2)' : 'rgba(255,255,255,0.05)',
                color: activeIndicators.ema20 ? '#22d3ee' : 'var(--text-muted)',
                border: activeIndicators.ema20 ? '1px solid #06b6d4' : '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.3rem 0.6rem',
                fontSize: '0.75rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              EMA 20
            </button>

            <button
              onClick={() => toggleIndicator('rsi')}
              style={{
                background: activeIndicators.rsi ? 'rgba(236, 72, 153, 0.2)' : 'rgba(255,255,255,0.05)',
                color: activeIndicators.rsi ? '#f472b6' : 'var(--text-muted)',
                border: activeIndicators.rsi ? '1px solid #ec4899' : '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.3rem 0.6rem',
                fontSize: '0.75rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              RSI (14)
            </button>

            <button
              onClick={() => toggleIndicator('macd')}
              style={{
                background: activeIndicators.macd ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255,255,255,0.05)',
                color: activeIndicators.macd ? '#34d399' : 'var(--text-muted)',
                border: activeIndicators.macd ? '1px solid #10b981' : '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.3rem 0.6rem',
                fontSize: '0.75rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              MACD
            </button>
          </div>

        </div>

        {/* Primary Stock Price & Indicators Line Chart */}
        <div style={{ height: '400px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={historyData} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="Date" stroke="#6b7280" tick={{ fontSize: 11 }} />
              <YAxis domain={['auto', 'auto']} stroke="#6b7280" tick={{ fontSize: 11 }} tickFormatter={(v) => `$${v}`} />
              <Tooltip
                contentStyle={{ background: '#111827', borderColor: '#374151', borderRadius: '8px', color: '#fff' }}
                formatter={(val, name) => [typeof val === 'number' ? `$${val.toFixed(2)}` : val, name]}
              />
              <Legend />
              
              <Line type="monotone" dataKey="Close" stroke="#6366f1" strokeWidth={2.5} dot={false} name="Close Price" />
              {activeIndicators.sma20 && <Line type="monotone" dataKey="SMA_20" stroke="#818cf8" strokeWidth={1.5} dot={false} strokeDasharray="4 4" name="SMA 20" />}
              {activeIndicators.sma50 && <Line type="monotone" dataKey="SMA_50" stroke="#fbbf24" strokeWidth={1.5} dot={false} strokeDasharray="4 4" name="SMA 50" />}
              {activeIndicators.ema20 && <Line type="monotone" dataKey="EMA_20" stroke="#22d3ee" strokeWidth={1.5} dot={false} name="EMA 20" />}
            </LineChart>
          </ResponsiveContainer>
        </div>

      </div>

      {/* Sub-Charts for Oscillators: RSI and MACD */}
      <div style={{ display: 'grid', gridTemplateColumns: activeIndicators.rsi && activeIndicators.macd ? '1fr 1fr' : '1fr', gap: '1.5rem' }}>
        
        {/* RSI Sub-Chart */}
        {activeIndicators.rsi && (
          <div className="glass-panel" style={{ padding: '1.25rem' }}>
            <h4 style={{ fontSize: '0.9rem', marginBottom: '1rem', color: 'var(--text-secondary)' }}>Relative Strength Index (RSI 14)</h4>
            <div style={{ height: '180px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={historyData} margin={{ top: 5, right: 20, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="Date" stroke="#6b7280" tick={{ fontSize: 10 }} />
                  <YAxis domain={[0, 100]} stroke="#6b7280" tick={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ background: '#111827', borderColor: '#374151', borderRadius: '8px' }} />
                  <ReferenceLine y={70} stroke="#f43f5e" strokeDasharray="3 3" label={{ value: 'Overbought (70)', fill: '#f43f5e', fontSize: 10 }} />
                  <ReferenceLine y={30} stroke="#10b981" strokeDasharray="3 3" label={{ value: 'Oversold (30)', fill: '#10b981', fontSize: 10 }} />
                  <Line type="monotone" dataKey="RSI_14" stroke="#ec4899" strokeWidth={2} dot={false} name="RSI" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* MACD Sub-Chart */}
        {activeIndicators.macd && (
          <div className="glass-panel" style={{ padding: '1.25rem' }}>
            <h4 style={{ fontSize: '0.9rem', marginBottom: '1rem', color: 'var(--text-secondary)' }}>MACD (12, 26, 9)</h4>
            <div style={{ height: '180px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={historyData} margin={{ top: 5, right: 20, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="Date" stroke="#6b7280" tick={{ fontSize: 10 }} />
                  <YAxis stroke="#6b7280" tick={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ background: '#111827', borderColor: '#374151', borderRadius: '8px' }} />
                  <Line type="monotone" dataKey="MACD" stroke="#10b981" strokeWidth={1.8} dot={false} name="MACD" />
                  <Line type="monotone" dataKey="MACD_Signal" stroke="#f59e0b" strokeWidth={1.8} dot={false} name="Signal" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

      </div>

    </div>
  );
}
