# backend/optionforge/api/strategies.py

from flask import request, jsonify
from . import api_bp
from optionforge.models import Strategy, User
from optionforge import db
from .utils import token_required

@api_bp.route('/strategies', methods=['POST'])
@token_required
def create_strategy(current_user):
    """Creates a new strategy for the logged-in user."""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('definition'):
        return jsonify({'message': 'Strategy name and definition are required'}), 400

    strategy = Strategy(
        name=data['name'],
        description=data.get('description', ''),
        definition=data['definition'],
        owner=current_user
    )
    db.session.add(strategy)
    db.session.commit()

    return jsonify({'message': 'Strategy created successfully', 'id': strategy.id}), 201

@api_bp.route('/strategies', methods=['GET'])
@token_required
def get_strategies(current_user):
    """Retrieves all strategies for the logged-in user."""
    strategies = Strategy.query.filter_by(user_id=current_user.id).all()
    output = []
    for strategy in strategies:
        strategy_data = {
            'id': strategy.id,
            'name': strategy.name,
            'description': strategy.description,
            'created_at': strategy.created_at
        }
        output.append(strategy_data)
    
    return jsonify({'strategies': output})

@api_bp.route('/strategies/<int:strategy_id>', methods=['GET'])
@token_required
def get_strategy(current_user, strategy_id):
    """Retrieves a single strategy."""
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=current_user.id).first()
    if not strategy:
        return jsonify({'message': 'Strategy not found'}), 404

    strategy_data = {
        'id': strategy.id,
        'name': strategy.name,
        'description': strategy.description,
        'definition': strategy.definition,
        'created_at': strategy.created_at
    }
    return jsonify(strategy_data)

@api_bp.route('/strategies/<int:strategy_id>', methods=['PUT'])
@token_required
def update_strategy(current_user, strategy_id):
    """Updates an existing strategy."""
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=current_user.id).first()
    if not strategy:
        return jsonify({'message': 'Strategy not found'}), 404

    data = request.get_json()
    strategy.name = data.get('name', strategy.name)
    strategy.description = data.get('description', strategy.description)
    strategy.definition = data.get('definition', strategy.definition)
    
    db.session.commit()
    return jsonify({'message': 'Strategy updated successfully'})

@api_bp.route('/strategies/<int:strategy_id>', methods=['DELETE'])
@token_required
def delete_strategy(current_user, strategy_id):
    """Deletes a strategy."""
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=current_user.id).first()
    if not strategy:
        return jsonify({'message': 'Strategy not found'}), 404
    
    db.session.delete(strategy)
    db.session.commit()
    return jsonify({'message': 'Strategy deleted successfully'})
