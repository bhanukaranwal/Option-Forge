# backend/optionforge/models.py

import datetime
import jwt
from flask import current_app
from optionforge import db, bcrypt

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    strategies = db.relationship('Strategy', backref='owner', lazy=True)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.registered_on = datetime.datetime.utcnow()
        self.is_admin = is_admin

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def encode_auth_token(self):
        """Generates the Auth Token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token"""
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return f'<User {self.email}>'


class Strategy(db.Model):
    """Stores user-defined options strategies."""
    __tablename__ = 'strategies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Stores the strategy definition as JSON
    definition = db.Column(db.JSON, nullable=False) 
    backtests = db.relationship('Backtest', backref='strategy', lazy='dynamic')

    def __repr__(self):
        return f'<Strategy {self.name}>'


class Backtest(db.Model):
    """Stores the results of a backtest run for a strategy."""
    __tablename__ = 'backtests'

    id = db.Column(db.Integer, primary_key=True)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategies.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='PENDING') # PENDING, RUNNING, COMPLETED, FAILED
    celery_task_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    # Stores the detailed results as JSON
    results = db.Column(db.JSON, nullable=True) 

    def __repr__(self):
        return f'<Backtest {self.id} for Strategy {self.strategy_id}>'


class OptionData(db.Model):
    """Stores historical options chain data."""
    __tablename__ = 'option_data'

    id = db.Column(db.Integer, primary_key=True)
    underlying_ticker = db.Column(db.String(10), nullable=False, index=True)
    data_date = db.Column(db.Date, nullable=False, index=True)
    expiration_date = db.Column(db.Date, nullable=False)
    strike_price = db.Column(db.Float, nullable=False)
    option_type = db.Column(db.String(4), nullable=False) # 'call' or 'put'
    
    last_price = db.Column(db.Float, nullable=True)
    bid = db.Column(db.Float, nullable=True)
    ask = db.Column(db.Float, nullable=True)
    volume = db.Column(db.Integer, nullable=True)
    open_interest = db.Column(db.Integer, nullable=True)
    implied_volatility = db.Column(db.Float, nullable=True)

    delta = db.Column(db.Float, nullable=True)
    gamma = db.Column(db.Float, nullable=True)
    theta = db.Column(db.Float, nullable=True)
    vega = db.Column(db.Float, nullable=True)

    __table_args__ = (db.UniqueConstraint('underlying_ticker', 'data_date', 'expiration_date', 'strike_price', 'option_type', name='_unique_option_contract'),)

    def __repr__(self):
        return f'<OptionData {self.underlying_ticker} {self.data_date} K={self.strike_price} {self.option_type}>'

