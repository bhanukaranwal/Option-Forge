// frontend/src/pages/BacktestResultsPage.tsx

import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '@/api/api';
import Card from '@/components/ui/Card';
import Plot from 'react-plotly.js';
import { useTheme } from '@/context/ThemeContext';
import toast from 'react-hot-toast';

// Dummy types - should match backend response
interface BacktestResults {
  summary_metrics: Record<string, number | string>;
  daily_pnl: { date: string; pnl: number }[];
}

const BacktestResultsPage = () => {
  const { backtestId } = useParams();
  const { theme } = useTheme();
  const [results, setResults] = useState<BacktestResults | null>(null);
  const [status, setStatus] = useState<string>('LOADING'); // LOADING, POLLING, COMPLETED, FAILED

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await apiClient.get(`/backtests/${backtestId}/results`);
        setResults(res.data);
        setStatus('COMPLETED');
      } catch (error: any) {
        if (error.response && error.response.status === 404) {
          // Not complete yet, start polling
          setStatus('POLLING');
        } else {
          console.error("Failed to fetch results", error);
          toast.error("Could not load backtest results.");
          setStatus('FAILED');
        }
      }
    };

    fetchResults();
  }, [backtestId]);
  
  useEffect(() => {
    let intervalId: number;
    if (status === 'POLLING') {
        toast('Backtest is running, polling for results...');
        intervalId = window.setInterval(async () => {
            try {
                const statusRes = await apiClient.get(`/backtests/${backtestId}/status`);
                if (statusRes.data.db_status === 'COMPLETED') {
                    setStatus('COMPLETED');
                    toast.success('Backtest complete! Fetching results.');
                    const resultsRes = await apiClient.get(`/backtests/${backtestId}/results`);
                    setResults(resultsRes.data);
                    clearInterval(intervalId);
                } else if (statusRes.data.db_status === 'FAILED') {
                    setStatus('FAILED');
                    toast.error('Backtest failed to complete.');
                    clearInterval(intervalId);
                }
            } catch (error) {
                console.error("Polling failed", error);
                setStatus('FAILED');
                toast.error('Error while checking backtest status.');
                clearInterval(intervalId);
            }
        }, 5000); // Poll every 5 seconds
    }
    return () => clearInterval(intervalId);
  }, [status, backtestId]);


  if (status === 'LOADING' || status === 'POLLING') {
    return (
        <Card>
            <h1 className="text-2xl font-bold mb-4">Backtest Results</h1>
            <p>{status === 'LOADING' ? 'Loading backtest data...' : 'Backtest in progress, waiting for completion...'}</p>
        </Card>
    );
  }
  
  if (status === 'FAILED' || !results) {
    return (
        <Card>
            <h1 className="text-2xl font-bold mb-4">Backtest Results</h1>
            <p className="text-red-500">Could not load or run the backtest. Please try again later.</p>
        </Card>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Backtest Results</h1>
      
      <Card>
        <h2 className="text-xl font-semibold mb-4">Summary Metrics</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {Object.entries(results.summary_metrics).map(([key, value]) => (
            <div key={key} className="p-4 bg-gray-100 dark:bg-slate-600 rounded-md">
              <p className="text-sm text-gray-500 dark:text-gray-400 capitalize">{key.replace(/_/g, ' ')}</p>
              <p className="text-2xl font-semibold">{value}</p>
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <h2 className="text-xl font-semibold mb-4">Equity Curve</h2>
        <Plot
          data={[
            {
              x: results.daily_pnl.map(d => d.date),
              y: results.daily_pnl.map(d => d.pnl),
              type: 'scatter',
              mode: 'lines',
              name: 'Portfolio Value'
            }
          ]}
          layout={{
            autosize: true,
            paper_bgcolor: theme === 'dark' ? '#334155' : '#ffffff',
            plot_bgcolor: theme === 'dark' ? '#334155' : '#ffffff',
            font: { color: theme === 'dark' ? '#f1f5f9' : '#0f172a' },
            xaxis: { title: 'Date' },
            yaxis: { title: 'Portfolio Value ($)' }
          }}
          useResizeHandler={true}
          className="w-full h-96"
        />
      </Card>
    </div>
  );
};

export default BacktestResultsPage;
