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
# Implementation of Logging
import logging
import os

# 1. Create a logs folder if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# 2. Configure the logger to write to a file
logging.basicConfig(
    filename='logs/himig.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 3. Create the logger object
logger = logging.getLogger(__name__)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

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
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        logger.info("Starting Himig ng Alaala API Server...")
    app.run(host="127.0.0.1", port=5000, debug=Config.DEBUG)
