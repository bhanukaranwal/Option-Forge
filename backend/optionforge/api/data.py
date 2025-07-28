# backend/optionforge/api/data.py

from flask import request, jsonify
from . import api_bp
from optionforge.models import OptionData
from .utils import token_required
import datetime

@api_bp.route('/data/option-chain', methods=['GET'])
@token_required
def get_option_chain(current_user):
    """
    Fetches the option chain for a given underlying and date.
    /api/data/option-chain?ticker=SPY&date=2023-01-20
    """
    ticker = request.args.get('ticker')
    date_str = request.args.get('date')

    if not ticker or not date_str:
        return jsonify({'message': 'Ticker and date parameters are required'}), 400

    try:
        data_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    chain_data = OptionData.query.filter_by(
        underlying_ticker=ticker.upper(),
        data_date=data_date
    ).order_by(OptionData.expiration_date, OptionData.strike_price).all()

    if not chain_data:
        return jsonify({'message': f'No data found for {ticker} on {date_str}'}), 404

    # Group by expiration date
    expirations = {}
    for option in chain_data:
        exp_date_str = option.expiration_date.strftime('%Y-%m-%d')
        if exp_date_str not in expirations:
            expirations[exp_date_str] = {'calls': [], 'puts': []}
        
        option_info = {
            'strike': option.strike_price,
            'lastPrice': option.last_price,
            'bid': option.bid,
            'ask': option.ask,
            'volume': option.volume,
            'openInterest': option.open_interest,
            'iv': option.implied_volatility,
            'delta': option.delta,
            'gamma': option.gamma,
            'theta': option.theta,
            'vega': option.vega,
        }

        if option.option_type == 'call':
            expirations[exp_date_str]['calls'].append(option_info)
        else:
            expirations[exp_date_str]['puts'].append(option_info)

    return jsonify(expirations)
