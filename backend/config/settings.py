"""
This handles all configuration settings for the backend application.

Responsibilities:
- Load environment variables from .env file
- Store API credentials (Spotify, future APIs)
- Define application-level settings (debug mode, cache limits, etc.)

Why this exists:
- Keeps sensitive data (API keys) out of the main code
- Makes configuration centralized and easy to manage
- Allows different settings for development vs production
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    # Enable debug mode (auto reload + error messages)
    DEBUG = True

    #Spotify API
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    #App Settings
    CACHE_LIMIT = 1000
    SPOTIFY_RESULT_LIMIT = 20 #change later after meeting

    #Soundcharts API
    SOUNDCHARTS_API_KEY = os.getenv("SOUNDCHARTS_API_KEY")

    #Validate if required environmental variables exist
    @staticmethod
    def validate():
        if not Config.SPOTIFY_CLIENT_ID:
            print("⚠️ Warning: SPOTIFY_CLIENT_ID not set")

        if not Config.SPOTIFY_CLIENT_SECRET:
            print("⚠️ Warning: SPOTIFY_CLIENT_SECRET not set")
