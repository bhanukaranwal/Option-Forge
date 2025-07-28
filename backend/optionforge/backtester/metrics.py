# backend/optionforge/backtester/metrics.py

import numpy as np
import pandas as pd

def calculate_metrics(pnl_series, risk_free_rate=0.02):
    """
    Calculates key performance metrics from a daily PnL series.

    :param pnl_series: A pandas Series of daily portfolio values or PnL.
    :param risk_free_rate: Annual risk-free rate for Sharpe/Sortino.
    :return: A dictionary of performance metrics.
    """
    if pnl_series.empty or len(pnl_series) < 2:
        return {
            'total_return_pct': 0, 'annualized_return_pct': 0, 'annualized_volatility_pct': 0,
            'sharpe_ratio': 0, 'sortino_ratio': 0, 'max_drawdown_pct': 0,
            'win_rate_pct': 0, 'profit_factor': 0, 'calmar_ratio': 0
        }

    # Ensure pnl_series represents cumulative returns/value
    if not (pnl_series.diff().dropna() == 0).all(): # if not already cumulative
        equity_curve = pnl_series.cumsum()
    else:
        equity_curve = pnl_series

    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1 if equity_curve.iloc[0] != 0 else 0
    
    daily_returns = equity_curve.pct_change().dropna()
    
    # Trading days per year
    trading_days = 252

    # Annualized Return
    num_days = len(equity_curve)
    annualized_return = (1 + total_return) ** (trading_days / num_days) - 1 if num_days > 0 else 0

    # Annualized Volatility
    annualized_volatility = daily_returns.std() * np.sqrt(trading_days)

    # Sharpe Ratio
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/trading_days) - 1
    excess_returns = daily_returns - daily_risk_free_rate
    sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(trading_days) if excess_returns.std() != 0 else 0

    # Sortino Ratio
    negative_returns = excess_returns[excess_returns < 0]
    downside_deviation = negative_returns.std() * np.sqrt(trading_days)
    sortino_ratio = (excess_returns.mean() * trading_days) / downside_deviation if downside_deviation != 0 else 0

    # Max Drawdown
    cumulative_max = equity_curve.cummax()
    drawdown = (equity_curve - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()

    # Calmar Ratio
    calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    # Win Rate & Profit Factor
    winning_days = daily_returns[daily_returns > 0]
    losing_days = daily_returns[daily_returns < 0]
    win_rate = len(winning_days) / len(daily_returns) if len(daily_returns) > 0 else 0
    
    total_profit = winning_days.sum()
    total_loss = abs(losing_days.sum())
    profit_factor = total_profit / total_loss if total_loss != 0 else np.inf

    return {
        'total_return_pct': round(total_return * 100, 2),
        'annualized_return_pct': round(annualized_return * 100, 2),
        'annualized_volatility_pct': round(annualized_volatility * 100, 2),
        'sharpe_ratio': round(sharpe_ratio, 2),
        'sortino_ratio': round(sortino_ratio, 2),
        'max_drawdown_pct': round(max_drawdown * 100, 2),
        'win_rate_pct': round(win_rate * 100, 2),
        'profit_factor': round(profit_factor, 2) if profit_factor != np.inf else 'inf',
        'calmar_ratio': round(calmar_ratio, 2)
    }

