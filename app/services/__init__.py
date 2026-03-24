from flask import Flask
from flask_restful import Api
import os

def create_app():
    """Application factory pattern for Flask app"""
    app = Flask(__name__)
    api = Api(app)
    
    # Import and register routes
    from app.routes import initialize_routes
    initialize_routes(api)
    
    return app