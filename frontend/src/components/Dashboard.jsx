import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CarbonCharts from './CarbonCharts';
import Analogies from './Analogies';
import { ShieldCheck, TrendingDown, Activity, DollarSign, Award, X, Dot } from 'lucide-react';

function EcoPassportModal({ isOpen, onClose, results }) {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden m-4">
        <div className="relative bg-gradient-to-br from-emerald-500 to-cyan-500 p-8 text-white text-center">
          <button onClick={onClose} className="absolute top-4 right-4 opacity-80 hover:opacity-100">
            <X className="w-6 h-6" />
          </button>
          <Award className="w-16 h-16 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">Eco-Passport</h2>
          <p className="text-emerald-100">Verified by Carbon Way</p>
        </div>
        <div className="p-8 space-y-6">
          <div className="text-center">
            <p className="text-gray-500 text-sm uppercase tracking-wider">Wallet Address</p>
            <p className="font-mono text-gray-700 mt-1">{results.address.slice(0, 6)}...{results.address.slice(-4)}</p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-2xl text-center">
              <p className="text-2xl font-bold text-gray-900">{results.total_co2.toFixed(4)}</p>
              <p className="text-xs text-gray-500 uppercase">kg CO₂</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-2xl text-center">
              <p className="text-2xl font-bold text-emerald-600">${results.offset_cost.toFixed(2)}</p>
              <p className="text-xs text-gray-500 uppercase">Offset Cost</p>
            </div>
          </div>
          <div className="text-center pt-4 border-t border-gray-100">
            <p className="text-gray-400 text-xs">
              Generated on {new Date(results.last_updated).toLocaleDateString()}
            </p>
            <div className="mt-4 inline-block px-4 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold">
              VERIFIED
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Dashboard({ results }) {
  const totalSavings = results.breakdown.reduce((acc, curr) => acc + curr.savings_l2, 0);
  const [showPassport, setShowPassport] = useState(false);
  const [offsetting, setOffsetting] = useState(false);
  const [syncStatus, setSyncStatus] = useState(null);

  useEffect(() => {
    const fetchSyncStatus = async () => {
      try {
        const response = await axios.get('/api/sync-status');
        setSyncStatus(response.data);
      } catch (e) {
        console.error('Failed to fetch sync status');
      }
    };
    fetchSyncStatus();
  }, []);

  const handleOffset = () => {
    setOffsetting(true);
    setTimeout(() => {
      setOffsetting(false);
      alert('Thank you for offsetting your carbon footprint! 🌱');
    }, 1500);
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Live Energy Mix Indicator */}
      <div className="flex justify-between items-center bg-white px-6 py-4 rounded-2xl shadow-sm border border-gray-100">
        <div className="flex items-center space-x-2">
          <div className="relative">
            <Dot className="w-5 h-5 text-emerald-500 fill-emerald-500" />
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-ping opacity-75" />
            </div>
          </div>
          <span className="font-semibold text-gray-800">Live Energy Mix</span>
        </div>
        {syncStatus && (
          <span className="text-sm text-gray-500">
            Synced {new Date(syncStatus.last_synced).toLocaleTimeString()}
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 flex items-start space-x-4">
          <div className="p-3 bg-emerald-100 rounded-2xl text-emerald-600">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Total Carbon Footprint</p>
            <p className="text-3xl font-bold text-gray-900">{results.total_co2.toFixed(4)} <span className="text-lg font-normal text-gray-400">kg CO₂</span></p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 flex items-start space-x-4">
          <div className="p-3 bg-blue-100 rounded-2xl text-blue-600">
            <TrendingDown className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">L2 Savings</p>
            <p className="text-3xl font-bold text-gray-900">{totalSavings.toFixed(4)} <span className="text-lg font-normal text-gray-400">kg CO₂</span></p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 flex items-start space-x-4">
          <div className="p-3 bg-purple-100 rounded-2xl text-purple-600">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Transactions Audited</p>
            <p className="text-3xl font-bold text-gray-900">
              {results.breakdown.reduce((acc, curr) => acc + curr.transactions, 0)}
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 flex items-start space-x-4">
          <div className="p-3 bg-amber-100 rounded-2xl text-amber-600">
            <DollarSign className="w-6 h-6" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-500">Carbon Offsetting</p>
            <p className="text-3xl font-bold text-gray-900 mb-2">${results.offset_cost.toFixed(2)}</p>
            <button 
              onClick={handleOffset}
              disabled={offsetting}
              className="w-full bg-emerald-600 text-white text-xs font-semibold py-2 rounded-xl hover:bg-emerald-700 disabled:bg-emerald-400 transition-colors"
            >
              {offsetting ? 'Processing...' : 'Offset Now'}
            </button>
          </div>
        </div>
      </div>

      <div className="text-right">
        <button 
          onClick={() => setShowPassport(true)}
          className="inline-flex items-center space-x-2 bg-white px-6 py-3 rounded-2xl shadow-sm border border-gray-200 text-gray-700 font-semibold hover:border-emerald-300 hover:text-emerald-700 transition-all"
        >
          <Award className="w-5 h-5" />
          <span>View Eco-Passport</span>
        </button>
      </div>

      <EcoPassportModal 
        isOpen={showPassport} 
        onClose={() => setShowPassport(false)} 
        results={results} 
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <CarbonCharts 
          breakdown={results.breakdown} 
          activityTypes={results.activity_types} 
        />
        <Analogies analogies={results.analogies} totalCo2={results.total_co2} />
      </div>
    </div>
  );
}

export default Dashboard;
