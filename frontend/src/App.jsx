import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Leaf, Loader2, AlertCircle } from 'lucide-react';
import Dashboard from './components/Dashboard';

const API_BASE = '/api'; // Proxied to localhost:8000

function App() {
  const [address, setAddress] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const validateAddress = (addr) => {
    return /^0x[a-fA-F0-9]{40}$/.test(addr);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!validateAddress(address)) {
      setError('Invalid Ethereum address format');
      return;
    }

    setError(null);
    setLoading(true);
    setResults(null);

    try {
      await axios.post(`${API_BASE}/analyze/${address}`);
      pollStatus(address);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start analysis');
      setLoading(false);
    }
  };

  const pollStatus = async (addr) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`${API_BASE}/status/${addr}`);
        setStatus(res.data.status);

        if (res.data.status === 'Completed') {
          clearInterval(interval);
          fetchResults(addr);
        } else if (res.data.status.startsWith('Error')) {
          clearInterval(interval);
          setError(res.data.status);
          setLoading(false);
        }
      } catch (err) {
        clearInterval(interval);
        setError('Connection lost while polling');
        setLoading(false);
      }
    }, 2000);
  };

  const fetchResults = async (addr) => {
    try {
      const res = await axios.get(`${API_BASE}/results/${addr}`);
      setResults(res.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch results');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="bg-white border-b border-gray-200 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Leaf className="w-8 h-8 text-emerald-500" />
            <h1 className="text-2xl font-bold tracking-tight text-gray-900">Carbon Way</h1>
          </div>
          <p className="text-sm text-gray-500 font-medium">Crypto Footprint Auditor</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="max-w-2xl mx-auto text-center mb-12">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl mb-4">
            Measure your Web3 Carbon Impact
          </h2>
          <p className="text-lg text-gray-600">
            Enter your wallet address to see the environmental impact of your transactions across Ethereum, Polygon, and Optimism.
          </p>
        </div>

        <form onSubmit={handleSearch} className="max-w-xl mx-auto mb-16">
          <div className="relative group">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400 group-focus-within:text-emerald-500 transition-colors" />
            </div>
            <input
              type="text"
              className={`block w-full pl-11 pr-32 py-4 bg-white border ${error ? 'border-red-300' : 'border-gray-300'} rounded-2xl leading-5 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm shadow-sm transition-all`}
              placeholder="0x..."
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !address}
              className="absolute right-2 top-2 bottom-2 px-6 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Analyze'}
            </button>
          </div>
          {error && (
            <div className="mt-4 flex items-center space-x-2 text-red-600 text-sm bg-red-50 p-3 rounded-lg border border-red-100">
              <AlertCircle className="w-4 h-4" />
              <span>{error}</span>
            </div>
          )}
          {loading && !results && (
            <div className="mt-6 text-center">
              <div className="inline-flex items-center space-x-3 text-emerald-700 font-medium">
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Status: {status || 'Initializing...'}</span>
              </div>
            </div>
          )}
        </form>

        {results && <Dashboard results={results} />}
      </main>
    </div>
  );
}

export default App;
