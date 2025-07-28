# backend/optionforge/api/backtests.py

from flask import request, jsonify, url_for
from . import api_bp
from optionforge.models import Backtest, Strategy
from optionforge import db
from .utils import token_required
from optionforge.tasks import run_backtest_task
import datetime

@api_bp.route('/strategies/<int:strategy_id>/backtests', methods=['POST'])
@token_required
def launch_backtest(current_user, strategy_id):
    """Launches a new backtest for a given strategy."""
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=current_user.id).first()
    if not strategy:
        return jsonify({'message': 'Strategy not found'}), 404

    data = request.get_json()
    if not data or not data.get('start_date') or not data.get('end_date'):
        return jsonify({'message': 'Start date and end date are required'}), 400

    try:
        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Create a new backtest record in the database
    new_backtest = Backtest(
        strategy_id=strategy.id,
        start_date=start_date,
        end_date=end_date,
        status='PENDING'
    )
    db.session.add(new_backtest)
    db.session.commit()

    # Launch the background task
    task = run_backtest_task.delay(new_backtest.id)

    # Store the Celery task ID
    new_backtest.celery_task_id = task.id
    db.session.commit()

    status_url = url_for('api.get_backtest_status', backtest_id=new_backtest.id, _external=True)

    return jsonify({
        'message': 'Backtest launched successfully.',
        'backtest_id': new_backtest.id,
        'task_id': task.id,
        'status_url': status_url
    }), 202

@api_bp.route('/backtests/<int:backtest_id>/status', methods=['GET'])
@token_required
def get_backtest_status(current_user, backtest_id):
    """Checks the status of a backtest."""
    backtest = Backtest.query.get_or_404(backtest_id)
    strategy = Strategy.query.get_or_404(backtest.strategy_id)

    if strategy.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    task = run_backtest_task.AsyncResult(backtest.celery_task_id)
    
    response = {
        'backtest_id': backtest.id,
        'status': task.state, # Celery state (PENDING, STARTED, SUCCESS, FAILURE)
        'db_status': backtest.status # Our custom status
    }

    if task.state == 'PENDING':
        response['info'] = 'Task is waiting to be processed.'
    elif task.state == 'STARTED':
        response['info'] = 'Task is currently running.'
    elif task.state != 'FAILURE':
        response['info'] = task.info if isinstance(task.info, str) else 'Task completed.'
        if task.state == 'SUCCESS':
            response['results_url'] = url_for('api.get_backtest_results', backtest_id=backtest.id, _external=True)

    else: # Failure case
        response['info'] = str(task.info) # Exception info

    return jsonify(response)


@api_bp.route('/backtests/<int:backtest_id>/results', methods=['GET'])
@token_required
def get_backtest_results(current_user, backtest_id):
    """Retrieves the results of a completed backtest."""
    backtest = Backtest.query.get_or_404(backtest_id)
    strategy = Strategy.query.get_or_404(backtest.strategy_id)

    if strategy.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    if backtest.status != 'COMPLETED':
        return jsonify({'message': 'Backtest is not yet complete.'}), 404

    return jsonify(backtest.results)

