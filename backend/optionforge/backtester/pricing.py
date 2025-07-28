# backend/optionforge/backtester/pricing.py

import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculates the Black-Scholes price for a European option.

    :param S: Current stock price
    :param K: Option strike price
    :param T: Time to expiration in years
    :param r: Risk-free interest rate
    :param sigma: Volatility of the underlying stock
    :param option_type: 'call' or 'put'
    :return: Option price
    """
    if T <= 0:
        return max(0, S - K) if option_type == 'call' else max(0, K - S)

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    elif option_type == 'put':
        price = (K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")
    
    return price

def black_scholes_greeks(S, K, T, r, sigma):
    """
    Calculates the Greeks for a European option.
    """
    if T <= 0:
        return {'delta_call': 1 if S > K else 0, 'delta_put': -1 if S < K else 0, 'gamma': 0, 'theta_call': 0, 'theta_put': 0, 'vega': 0}

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Gamma is the same for calls and puts
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))

    # Vega is the same for calls and puts
    vega = S * norm.pdf(d1) * np.sqrt(T) * 0.01 # per 1% change in vol

    # Delta
    delta_call = norm.cdf(d1)
    delta_put = delta_call - 1

    # Theta (per day)
    theta_call = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365

    return {
        'delta_call': delta_call,
        'delta_put': delta_put,
        'gamma': gamma,
        'theta_call': theta_call,
        'theta_put': theta_put,
        'vega': vega
    }
