// frontend/src/pages/DashboardPage.tsx

import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '@/api/api';
import { PlusIcon } from '@heroicons/react/24/solid';
import Card from '@/components/ui/Card';

interface Strategy {
  id: number;
  name: string;
  description: string;
  created_at: string;
}

const DashboardPage = () => {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchStrategies = async () => {
      try {
        const response = await apiClient.get('/strategies');
        setStrategies(response.data.strategies);
      } catch (error) {
        console.error("Failed to fetch strategies", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchStrategies();
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-text-light dark:text-text-dark">My Strategies</h1>
        <Link
          to="/strategy/new"
          className="inline-flex items-center px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-hover"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          New Strategy
        </Link>
      </div>
      
      {isLoading ? (
        <p>Loading strategies...</p>
      ) : strategies.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {strategies.map(strategy => (
            <Card key={strategy.id}>
              <h2 className="text-xl font-semibold mb-2">{strategy.name}</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-4 flex-grow">{strategy.description}</p>
              <div className="flex justify-between items-center mt-4">
                <span className="text-sm text-gray-500">
                  Created: {new Date(strategy.created_at).toLocaleDateString()}
                </span>
                <div>
                  <Link to={`/strategy/${strategy.id}/edit`} className="text-sm font-medium text-primary hover:underline mr-4">Edit</Link>
                  <button className="text-sm font-medium text-green-500 hover:underline">Backtest</button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
            <h3 className="text-xl font-medium">No Strategies Found</h3>
            <p className="text-gray-500 mt-2">Get started by creating your first options strategy.</p>
            <Link
              to="/strategy/new"
              className="mt-4 inline-flex items-center px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-hover"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Create Strategy
            </Link>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
