// frontend/src/components/layout/Sidebar.tsx

import { NavLink } from 'react-router-dom';
import { ChartBarIcon, Cog6ToothIcon, DocumentPlusIcon, HomeIcon } from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Strategy Builder', href: '/strategy/new', icon: DocumentPlusIcon },
  { name: 'Backtests', href: '/backtests', icon: ChartBarIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
];

const Sidebar = () => {
  return (
    <div className="w-64 bg-card-light dark:bg-card-dark border-r border-border-light dark:border-border-dark flex flex-col">
      <div className="flex items-center justify-center h-20 border-b border-border-light dark:border-border-dark">
        <h1 className="text-2xl font-bold text-primary">OptionForge</h1>
      </div>
      <nav className="flex-1 px-2 py-4 space-y-2">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            end={item.href === '/'}
            className={({ isActive }) =>
              `flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                isActive
                  ? 'bg-primary text-white'
                  : 'text-text-light dark:text-text-dark hover:bg-gray-200 dark:hover:bg-slate-700'
              }`
            }
          >
            <item.icon className="h-6 w-6 mr-3" />
            {item.name}
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
