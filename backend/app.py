"""
This is the main entry point of the backend application.

Responsibilities:
- Initialize the Flask app
- Load configuration settings
- Enable CORS (so frontend can communicate with backend)
- Register all route blueprints
"""

from flask import Flask
from flask_cors import CORS
from routes.survey_routes import survey_bp
from config.settings import Config


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # Enable CORS for frontend integration
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register survey routes
    app.register_blueprint(survey_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=Config.DEBUG)