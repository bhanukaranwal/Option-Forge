# scripts/seed_data.py

import datetime
import time
import yfinance as yf
import pandas as pd
from contextlib import contextmanager

# This is a standalone script. To run it, we need to set up the app context.
# This allows the script to access the Flask app's configuration and extensions (like SQLAlchemy).
import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from optionforge import create_app, db
from optionforge.models import User, Strategy, OptionData

# --- Configuration ---
# How many years of data to fetch. Be careful, this can be very large.
YEARS_OF_DATA = 2 
# Tickers to fetch data for. Should match the .env file.
TICKERS = os.environ.get('YFINANCE_TICKERS', "SPY QQQ").split()
# Default user credentials
DEFAULT_USER_EMAIL = "trader@example.com"
DEFAULT_USER_PASSWORD = "password123"


@contextmanager
def app_context():
    """Provides a Flask application context for the script."""
    app = create_app()
    with app.app_context():
        yield

def clear_data():
    """Clears existing data from the tables."""
    print("Clearing existing data...")
    # Order matters due to foreign key constraints
    OptionData.query.delete()
    Strategy.query.delete()
    User.query.delete()
    db.session.commit()
    print("Data cleared.")

def create_default_user():
    """Creates a default user for the application."""
    print(f"Checking for default user: {DEFAULT_USER_EMAIL}")
    user = User.query.filter_by(email=DEFAULT_USER_EMAIL).first()
    if not user:
        print("Default user not found. Creating...")
        user = User(email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD)
        db.session.add(user)
        db.session.commit()
        print("Default user created.")
    else:
        print("Default user already exists.")
    return user

def create_sample_strategies(user):
    """Creates some example strategies for the default user."""
    print("Creating sample strategies...")
    
    strategies = [
        {
            "name": "SPY Short Straddle",
            "description": "A classic short volatility strategy. Sell an at-the-money call and put with the same expiration.",
            "definition": {
                "underlying_ticker": "SPY",
                "legs": [
                    {"type": "call", "action": "sell", "quantity": 1, "delta": 0.5, "dte": 45},
                    {"type": "put", "action": "sell", "quantity": 1, "delta": -0.5, "dte": 45}
                ],
                "entry_rules": {"time_of_day": "10:00", "days_of_week": [1,2,3,4,5]},
                "exit_rules": {"profit_target_pct": 50, "stop_loss_pct": 100, "dte_to_exit": 21}
            }
        },
        {
            "name": "QQQ Iron Condor",
            "description": "A defined-risk, neutral strategy. Sells an out-of-the-money put spread and call spread.",
            "definition": {
                "underlying_ticker": "QQQ",
                "legs": [
                    {"type": "put", "action": "sell", "quantity": 1, "delta": -0.10, "dte": 45},
                    {"type": "put", "action": "buy", "quantity": 1, "strike_offset": -5, "dte": 45},
                    {"type": "call", "action": "sell", "quantity": 1, "delta": 0.10, "dte": 45},
                    {"type": "call", "action": "buy", "quantity": 1, "strike_offset": 5, "dte": 45}
                ],
                "entry_rules": {"iv_rank_min": 30},
                "exit_rules": {"profit_target_pct": 50, "stop_loss_pct": 100, "dte_to_exit": 10}
            }
        },
        {
            "name": "SPY Bull Call Spread",
            "description": "A defined-risk, bullish strategy. Buy a call and sell a higher-strike call to finance it.",
            "definition": {
                "underlying_ticker": "SPY",
                "legs": [
                    {"type": "call", "action": "buy", "quantity": 1, "delta": 0.7, "dte": 60},
                    {"type": "call", "action": "sell", "quantity": 1, "delta": 0.4, "dte": 60}
                ],
                "entry_rules": {"moving_average_cross": {"short": 20, "long": 50}},
                "exit_rules": {"profit_target_pct": 100, "stop_loss_pct": 50}
            }
        }
    ]

    for strat_data in strategies:
        exists = Strategy.query.filter_by(name=strat_data["name"], user_id=user.id).first()
        if not exists:
            new_strat = Strategy(
                name=strat_data["name"],
                description=strat_data["description"],
                definition=strat_data["definition"],
                owner=user
            )
            db.session.add(new_strat)
    
    db.session.commit()
    print(f"{len(strategies)} sample strategies created/verified.")


def fetch_and_store_options_data():
    """Fetches historical options data from yfinance and stores it in the DB."""
    print(f"Starting data fetch for tickers: {TICKERS}")
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365 * YEARS_OF_DATA)
    
    for ticker_symbol in TICKERS:
        print(f"\n--- Processing {ticker_symbol} ---")
        ticker = yf.Ticker(ticker_symbol)
        
        # Get historical data to iterate through trading days
        hist = ticker.history(start=start_date, end=end_date)
        if hist.empty:
            print(f"Could not get history for {ticker_symbol}. Skipping.")
            continue
            
        print(f"Found {len(hist)} trading days between {start_date} and {end_date}.")

        for trading_date in hist.index.date:
            date_str = trading_date.strftime('%Y-%m-%d')
            print(f"Fetching options for {date_str}...")
            
            # Check if we already have data for this day
            if OptionData.query.filter_by(underlying_ticker=ticker_symbol, data_date=trading_date).first():
                print(f"Data for {date_str} already exists. Skipping.")
                continue

            try:
                # yfinance fetches options per expiration date
                expirations = ticker.options
                if not expirations:
                    print(f"No expirations found for {date_str}. Skipping.")
                    continue
                
                all_options = []
                for exp in expirations:
                    opt_chain = ticker.option_chain(exp)
                    
                    # Combine calls and puts
                    df = pd.concat([opt_chain.calls, opt_chain.puts])
                    df['optionType'] = df['contractSymbol'].str.extract(r'\d([CP])')
                    df['optionType'] = df['optionType'].map({'C': 'call', 'P': 'put'})
                    
                    # Add necessary columns
                    df['underlyingTicker'] = ticker_symbol
                    df['dataDate'] = trading_date
                    df['expirationDate'] = pd.to_datetime(exp).date()
                    
                    all_options.append(df)
                
                if not all_options:
                    continue

                full_chain = pd.concat(all_options)
                
                # Clean and format data for DB insertion
                records_to_insert = []
                for _, row in full_chain.iterrows():
                    records_to_insert.append(OptionData(
                        underlying_ticker=row['underlyingTicker'],
                        data_date=row['dataDate'],
                        expiration_date=row['expirationDate'],
                        strike_price=row['strike'],
                        option_type=row['optionType'],
                        last_price=row.get('lastPrice'),
                        bid=row.get('bid'),
                        ask=row.get('ask'),
                        volume=row.get('volume'),
                        open_interest=row.get('openInterest'),
                        implied_volatility=row.get('impliedVolatility')
                        # Greeks are not reliably provided by yfinance for historical data
                    ))
                
                # Bulk insert for efficiency
                db.session.bulk_save_objects(records_to_insert)
                db.session.commit()
                print(f"Successfully stored {len(records_to_insert)} option contracts for {date_str}.")
                
                # yfinance can be sensitive to rapid requests
                time.sleep(2)

            except Exception as e:
                print(f"Could not fetch options for {date_str}. Error: {e}")
                db.session.rollback()
                time.sleep(5) # Wait longer after an error

    print("\nData fetching complete.")


if __name__ == "__main__":
    with app_context():
        # The order of operations is important
        # 1. Clear old data (optional, for clean slate)
        # clear_data() # Uncomment to wipe the DB before seeding
        
        # 2. Create a user to own the strategies
        user = create_default_user()
        
        # 3. Create sample strategies
        create_sample_strategies(user)
        
        # 4. Fetch and store historical market data
        fetch_and_store_options_data()
        
        print("\nDatabase seeding finished successfully!")
