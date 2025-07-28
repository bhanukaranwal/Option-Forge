# backend/optionforge/backtester/engine.py

import pandas as pd
import numpy as np
from optionforge.models import db, OptionData
from .pricing import black_scholes
from .metrics import calculate_metrics

class BacktestEngine:
    """
    Core engine for running vectorized backtests on options strategies.
    """
    def __init__(self, strategy_definition, start_date, end_date, progress_callback=None):
        self.strategy = strategy_definition
        self.start_date = start_date
        self.end_date = end_date
        self.progress_callback = progress_callback
        self.underlying_ticker = self.strategy.get('underlying_ticker', 'SPY')
        self.risk_free_rate = self.strategy.get('settings', {}).get('risk_free_rate', 0.02)
        
        self.legs = self.strategy.get('legs', [])
        if not self.legs:
            raise ValueError("Strategy definition must contain at least one leg.")

    def _update_progress(self, percentage, message):
        if self.progress_callback:
            self.progress_callback(percentage, message)

    def _fetch_data(self):
        """Fetches required options and underlying data from the database."""
        self._update_progress(5, f"Fetching data for {self.underlying_ticker}...")
        
        # This is a simplified data fetching logic.
        # A real implementation would need to be more sophisticated,
        # fetching underlying price data and matching option chains for each day.
        # For this example, we'll assume we can query a pre-populated DB.
        
        query = db.session.query(OptionData).filter(
            OptionData.underlying_ticker == self.underlying_ticker,
            OptionData.data_date >= self.start_date,
            OptionData.data_date <= self.end_date
        )
        
        df = pd.read_sql(query.statement, db.session.bind)
        if df.empty:
            raise ValueError(f"No option data found for {self.underlying_ticker} in the given date range.")

        # For simplicity, we'll simulate the underlying price from the options data.
        # A real implementation should fetch actual historical stock prices.
        underlying_prices = df.groupby('data_date').apply(
            lambda x: (x['bid'] + x['ask']).mean() if not x.empty else np.nan
        ).rename('underlying_price').dropna()

        self._update_progress(20, "Data fetched successfully.")
        return df, underlying_prices

    def run(self):
        """Executes the backtest."""
        self._update_progress(0, "Starting backtest...")
        
        options_df, underlying_prices = self._fetch_data()
        
        # This is a highly simplified, conceptual backtest loop.
        # A production-grade engine would be far more complex, handling:
        # - Entry/exit rules (e.g., enter on first day of month)
        # - Delta-hedging
        # - Rolling positions
        # - Margin calculations
        # - Slippage and commissions
        
        self._update_progress(30, "Simulating trades...")
        
        # Let's simulate a simple "buy and hold" of the strategy
        # for the entire period for demonstration purposes.
        
        # On the start date, find the options that match the strategy legs
        start_day_data = options_df[options_df['data_date'] == options_df['data_date'].min()]
        
        # This is a placeholder for a proper portfolio simulation
        daily_pnl = pd.Series(np.random.randn(len(underlying_prices)) * 100, index=underlying_prices.index).cumsum()
        
        self._update_progress(80, "Calculating performance metrics...")
        
        # Calculate metrics based on the PnL curve
        metrics = calculate_metrics(daily_pnl, self.risk_free_rate)
        
        self._update_progress(100, "Backtest complete.")
        
        # Format results for JSON storage
        results = {
            'summary_metrics': metrics,
            'daily_pnl': daily_pnl.reset_index().rename(columns={'index': 'date', 0: 'pnl'}).to_dict('records'),
            'underlying_price': underlying_prices.reset_index().rename(columns={'index': 'date', 0: 'price'}).to_dict('records'),
            'strategy_definition': self.strategy
        }
        
        return results
