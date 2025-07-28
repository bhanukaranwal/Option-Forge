// frontend/src/pages/StrategyBuilderPage.tsx

import React, { useState } from 'react';
import Card from '@/components/ui/Card';
import Plot from 'react-plotly.js';
import { useTheme } from '@/context/ThemeContext';

// This is a placeholder for the complex strategy builder UI.
// A real implementation would involve drag-and-drop, complex forms,
// and state management for the strategy definition.

const StrategyBuilderPage = () => {
  const { theme } = useTheme();
  const [legs, setLegs] = useState([
    { id: 1, type: 'call', action: 'buy', quantity: 1, strike: 150 },
    { id: 2, type: 'call', action: 'sell', quantity: 1, strike: 155 },
  ]);

  // Dummy payoff calculation
  const calculatePayoff = () => {
    const underlyingRange = Array.from({ length: 101 }, (_, i) => 125 + i * 0.5); // Prices from 125 to 175
    const payoff = underlyingRange.map(price => {
      let legPayoff = 0;
      for (const leg of legs) {
        let p = 0;
        if (leg.type === 'call') {
          p = Math.max(0, price - leg.strike);
        } else { // put
          p = Math.max(0, leg.strike - price);
        }
        legPayoff += (leg.action === 'buy' ? p : -p) * leg.quantity;
      }
      return legPayoff;
    });
    return { underlyingRange, payoff };
  };

  const { underlyingRange, payoff } = calculatePayoff();

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Strategy Builder</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Panel: Strategy Legs */}
        <div className="lg:col-span-1 space-y-4">
          <Card>
            <h2 className="text-xl font-semibold mb-4">Strategy Legs</h2>
            {legs.map(leg => (
              <div key={leg.id} className="flex justify-between items-center p-2 border-b border-border-light dark:border-border-dark">
                <span>{leg.quantity}x {leg.strike} {leg.type}</span>
                <span className={`capitalize font-semibold ${leg.action === 'buy' ? 'text-green-500' : 'text-red-500'}`}>{leg.action}</span>
              </div>
            ))}
            <button className="mt-4 w-full py-2 bg-gray-200 dark:bg-slate-600 rounded-md">Add Leg</button>
          </Card>
          <Card>
             <h2 className="text-xl font-semibold mb-4">Entry & Exit Rules</h2>
             <p className="text-gray-500">Configuration for entry/exit rules will be here.</p>
          </Card>
        </div>

        {/* Right Panel: Payoff Diagram */}
        <div className="lg:col-span-2">
          <Card>
            <h2 className="text-xl font-semibold mb-4">Payoff Diagram at Expiration</h2>
            <Plot
              data={[
                {
                  x: underlyingRange,
                  y: payoff,
                  type: 'scatter',
                  mode: 'lines',
                  line: { color: '#3b82f6' },
                  name: 'Payoff'
                },
                {
                  x: [underlyingRange[0], underlyingRange[underlyingRange.length - 1]],
                  y: [0, 0],
                  type: 'scatter',
                  mode: 'lines',
                  line: { color: 'grey', dash: 'dash' },
                  name: 'Zero P/L'
                }
              ]}
              layout={{
                autosize: true,
                paper_bgcolor: theme === 'dark' ? '#334155' : '#ffffff',
                plot_bgcolor: theme === 'dark' ? '#334155' : '#ffffff',
                font: {
                  color: theme === 'dark' ? '#f1f5f9' : '#0f172a'
                },
                xaxis: { title: 'Underlying Price at Expiration' },
                yaxis: { title: 'Profit / Loss' },
                showlegend: false,
              }}
              useResizeHandler={true}
              className="w-full h-96"
            />
          </Card>
        </div>
      </div>
    </div>
  );
};

export default StrategyBuilderPage;
