# backend/optionforge/api/__init__.py

from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import routes to register them with the blueprint
from . import auth, strategies, backtests, data
