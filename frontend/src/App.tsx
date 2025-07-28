// frontend/src/App.tsx

import { Routes, Route } from 'react-router-dom';
import {
  DashboardPage,
  LoginPage,
  RegisterPage,
  StrategyBuilderPage,
  BacktestResultsPage,
  NotFoundPage,
  SettingsPage
} from './pages';
import MainLayout from './layouts/MainLayout';
import ProtectedRoute from './components/auth/ProtectedRoute';
import { ThemeProvider } from './context/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected Routes */}
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardPage />} />
          <Route path="strategy/new" element={<StrategyBuilderPage />} />
          <Route path="strategy/:strategyId/edit" element={<StrategyBuilderPage />} />
          <Route path="backtest/:backtestId" element={<BacktestResultsPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;
