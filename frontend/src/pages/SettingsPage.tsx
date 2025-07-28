// frontend/src/pages/SettingsPage.tsx

import Card from '@/components/ui/Card';

const SettingsPage = () => {
  // In a real app, these values would be fetched from a user profile API
  // and be updatable.
  const settings = {
    riskFreeRate: 2.0,
    commissionPerContract: 0.65,
    slippagePct: 0.1,
    defaultVolModel: 'Black-Scholes',
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Settings</h1>
      <Card>
        <div className="max-w-md space-y-6">
          <div>
            <label className="block text-sm font-medium">Risk-Free Rate (%)</label>
            <input
              type="number"
              defaultValue={settings.riskFreeRate}
              className="mt-1 w-full p-2 bg-gray-100 dark:bg-slate-600 border border-border-light dark:border-border-dark rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Commission per Contract ($)</label>
            <input
              type="number"
              defaultValue={settings.commissionPerContract}
              className="mt-1 w-full p-2 bg-gray-100 dark:bg-slate-600 border border-border-light dark:border-border-dark rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Slippage (%)</label>
            <input
              type="number"
              defaultValue={settings.slippagePct}
              className="mt-1 w-full p-2 bg-gray-100 dark:bg-slate-600 border border-border-light dark:border-border-dark rounded-md"
            />
          </div>
          <button className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-hover">
            Save Settings
          </button>
        </div>
      </Card>
    </div>
  );
};

export default SettingsPage;
