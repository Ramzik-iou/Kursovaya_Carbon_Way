import React from 'react';
import { 
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';
import { Repeat, Leaf, Send } from 'lucide-react';

const COLORS = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b'];
const ACTIVITY_COLORS = {
  'DeFi': '#3b82f6',
  'NFT': '#8b5cf6',
  'Transfer': '#10b981'
};

function CarbonCharts({ breakdown, activityTypes }) {
  const pieData = breakdown.map(item => ({
    name: item.network,
    value: item.co2
  }));

  const barData = breakdown.map(item => ({
    name: item.network,
    Actual: item.co2,
    Hypothetical: item.co2 + item.savings_l2
  }));

  const activityData = activityTypes ? Object.entries(activityTypes).map(([key, value]) => ({
    name: key,
    value: value.co2
  })) : [];

  const getActivityIcon = (name) => {
    switch (name) {
      case 'DeFi': return <Repeat className="w-4 h-4 inline mr-1" />;
      case 'NFT': return <Leaf className="w-4 h-4 inline mr-1" />;
      case 'Transfer': return <Send className="w-4 h-4 inline mr-1" />;
      default: return null;
    }
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
        <h3 className="text-xl font-bold mb-6 text-gray-900">Footprint by Activity Type</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={activityData}
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={90}
                paddingAngle={5}
                dataKey="value"
              >
                {activityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={ACTIVITY_COLORS[entry.name] || COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value) => [`${value.toFixed(4)} kg CO₂`, 'Footprint']}
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              />
              <Legend 
                verticalAlign="bottom" 
                height={36}
                formatter={(value) => (
                  <span className="flex items-center text-gray-700">
                    {getActivityIcon(value)} {value}
                  </span>
                )}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
        <h3 className="text-xl font-bold mb-6 text-gray-900">Footprint by Network</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              />
              <Legend verticalAlign="bottom" height={36}/>
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
        <h3 className="text-xl font-bold mb-6 text-gray-900">L2 Savings Impact</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#9ca3af'}} />
              <YAxis axisLine={false} tickLine={false} tick={{fill: '#9ca3af'}} />
              <Tooltip 
                cursor={{fill: '#f9fafb'}}
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              />
              <Legend verticalAlign="bottom" height={36}/>
              <Bar dataKey="Actual" fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Hypothetical" fill="#d1d5db" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <p className="mt-4 text-sm text-gray-500 italic text-center">
          "Hypothetical" shows what the footprint would be if all transactions were on Ethereum Mainnet.
        </p>
      </div>
    </div>
  );
}

export default CarbonCharts;
