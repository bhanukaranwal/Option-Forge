# backend/optionforge/tasks.py

from . import celery, create_app
from .models import db, Backtest
from .backtester.engine import BacktestEngine
import datetime

# Create a Flask app context for the celery worker
app = create_app()
app.app_context().push()

@celery.task(bind=True)
def run_backtest_task(self, backtest_id):
    """
    Celery task to execute an options strategy backtest.
    """
    backtest = Backtest.query.get(backtest_id)
    if not backtest:
        self.update_state(state='FAILURE', meta={'exc_type': 'NotFound', 'exc_message': 'Backtest ID not found.'})
        return

    try:
        # Update status in DB
        backtest.status = 'RUNNING'
        db.session.commit()
        self.update_state(state='STARTED', meta={'current': 0, 'total': 100, 'status': 'Initializing...'})

        # Initialize the backtesting engine
        engine = BacktestEngine(
            strategy_definition=backtest.strategy.definition,
            start_date=backtest.start_date,
            end_date=backtest.end_date,
            # Pass a progress update callback to the engine
            progress_callback=lambda p, m: self.update_state(state='PROGRESS', meta={'current': p, 'total': 100, 'status': m})
        )
        
        # Run the backtest
        results = engine.run()

        # Store results and update status
        backtest.results = results
        backtest.status = 'COMPLETED'
        backtest.completed_at = datetime.datetime.utcnow()
        db.session.commit()

        return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': backtest.id}

    except Exception as e:
        backtest.status = 'FAILED'
        db.session.commit()
        # Log the exception
        print(f"Backtest task {backtest_id} failed: {e}")
        self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e)})
        # Re-raise the exception so Celery knows it failed
        raise e

