import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import TSAnalysis from './components/TSAnalysis';
import MLPrediction from './components/MLPrediction';
import { API_BASE_URL } from './config';

export default function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [period, setPeriod] = useState('2y');
  const [activeTab, setActiveTab] = useState('dashboard');

  const [stockInfo, setStockInfo] = useState(null);
  const [historyData, setHistoryData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState(false);

  // Check API health status
  const checkApiHealth = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/`);
      if (res.ok) {
        setApiStatus(true);
      } else {
        setApiStatus(false);
      }
    } catch {
      setApiStatus(false);
    }
  };

  // Fetch stock details and price history
  const fetchStockData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch info metadata
      const infoRes = await fetch(`${API_BASE_URL}/api/stock/info?ticker=${ticker}`);
      if (infoRes.ok) {
        const infoData = await infoRes.json();
        setStockInfo(infoData);
      }

      // 2. Fetch history and indicators
      const histRes = await fetch(`${API_BASE_URL}/api/stock/history?ticker=${ticker}&period=${period}`);
      if (!histRes.ok) {
        const errJson = await histRes.json();
        throw new Error(errJson.detail || `Failed to load stock data for ${ticker}`);
      }

      const histJson = await histRes.json();
      setHistoryData(histJson.data || []);
      setApiStatus(true);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Error fetching stock data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkApiHealth();
    fetchStockData();
  }, [ticker, period]);

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Navigation Header */}
      <Navbar
        currentTicker={ticker}
        setTicker={setTicker}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiStatus={apiStatus}
      />

      {/* Main App Container */}
      <main style={{ flex: 1, maxWidth: '1400px', width: '100%', margin: '0 auto', padding: '0 1.5rem 3rem 1.5rem' }}>
        
        {error && (
          <div className="glass-panel" style={{ padding: '1rem 1.5rem', marginBottom: '1.5rem', borderColor: 'var(--accent-danger)', color: 'var(--accent-danger)' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Tab View Routing */}
        {activeTab === 'dashboard' && (
          <Dashboard
            stockInfo={stockInfo}
            historyData={historyData}
            period={period}
            setPeriod={setPeriod}
            loading={loading}
          />
        )}

        {activeTab === 'ts' && (
          <TSAnalysis
            ticker={ticker}
            historyData={historyData}
          />
        )}

        {activeTab === 'ml' && (
          <MLPrediction
            ticker={ticker}
          />
        )}

      </main>

      {/* Footer */}
      <footer style={{ textAlign: 'center', padding: '1.5rem', color: 'var(--text-muted)', fontSize: '0.8rem', borderTop: '1px solid var(--border-color)' }}>
        Stock Trend Prediction & Time Series Analysis Capstone Project &copy; {new Date().getFullYear()}
      </footer>

    </div>
  );
}
