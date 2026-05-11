import React from 'react';
import { Coffee, Car, TreeDeciduous } from 'lucide-react';

function Analogies({ analogies, totalCo2 }) {
  return (
    <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 h-full">
      <h3 className="text-xl font-bold mb-8 text-gray-900">What does this mean?</h3>
      
      <div className="space-y-8">
        <div className="flex items-center space-x-6 p-4 rounded-2xl hover:bg-gray-50 transition-colors">
          <div className="p-4 bg-orange-100 rounded-2xl text-orange-600">
            <Coffee className="w-8 h-8" />
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">{analogies.kettle_hours}</p>
            <p className="text-sm text-gray-500 font-medium uppercase tracking-wider">Hours of boiling a kettle</p>
          </div>
        </div>

        <div className="flex items-center space-x-6 p-4 rounded-2xl hover:bg-gray-50 transition-colors">
          <div className="p-4 bg-blue-100 rounded-2xl text-blue-600">
            <Car className="w-8 h-8" />
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">{analogies.ev_km}</p>
            <p className="text-sm text-gray-500 font-medium uppercase tracking-wider">Kilometers in an Electric Vehicle</p>
          </div>
        </div>

        <div className="flex items-center space-x-6 p-4 rounded-2xl hover:bg-gray-50 transition-colors">
          <div className="p-4 bg-emerald-100 rounded-2xl text-emerald-600">
            <TreeDeciduous className="w-8 h-8" />
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">{analogies.tree_days}</p>
            <p className="text-sm text-gray-500 font-medium uppercase tracking-wider">Days for one tree to absorb</p>
          </div>
        </div>
      </div>

      <div className="mt-12 p-6 bg-emerald-50 rounded-2xl border border-emerald-100">
        <p className="text-emerald-800 text-sm leading-relaxed">
          <strong>Tip:</strong> You can reduce your carbon footprint by bridging to Layer 2 networks like Optimism or using PoS networks like Polygon. 
          Post-merge Ethereum is also 99.9% more energy efficient than before!
        </p>
      </div>
    </div>
  );
}

export default Analogies;
