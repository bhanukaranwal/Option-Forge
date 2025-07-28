# backend/optionforge/main/routes.py

from flask import jsonify, current_app
from . import main

@main.route('/')
def index():
    """Serves a simple welcome message or API status."""
    return jsonify({
        "message": "Welcome to the OptionForge API!",
        "version": "1.0.0",
        "docs": "/docs"
    })

@main.route('/docs')
def get_docs():
    """Redirects to the Swagger UI documentation."""
    # This will eventually serve the Swagger UI HTML file
    # For now, it's a placeholder
    return "Swagger UI documentation will be here.", 200

@main.route('/openapi.json')
def openapi_spec():
    """Serves the OpenAPI specification."""
    # In a real app, you'd generate this with apispec
    # For now, a placeholder
    return jsonify({"openapi": "3.0.0", "info": {"title": "OptionForge API", "version": "1.0"}, "paths": {}}), 200
