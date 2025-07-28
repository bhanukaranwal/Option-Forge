// frontend/src/components/layout/Header.tsx

import { SunIcon, MoonIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline';
import { useAuth } from '@/hooks/useAuth';
import { useTheme } from '@/context/ThemeContext';

const Header = () => {
  const { logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="bg-card-light dark:bg-card-dark shadow-md p-4 flex justify-between items-center border-b border-border-light dark:border-border-dark">
      <div>
        {/* Breadcrumbs or Page Title can go here */}
        <h1 className="text-xl font-semibold text-text-light dark:text-text-dark">Dashboard</h1>
      </div>
      <div className="flex items-center space-x-4">
        <button onClick={toggleTheme} className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-slate-600">
          {theme === 'light' ? (
            <MoonIcon className="h-6 w-6 text-slate-600" />
          ) : (
            <SunIcon className="h-6 w-6 text-yellow-400" />
          )}
        </button>
        <button onClick={logout} className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-slate-600">
          <ArrowRightOnRectangleIcon className="h-6 w-6 text-slate-600 dark:text-slate-300" />
        </button>
      </div>
    </header>
  );
};

export default Header;
