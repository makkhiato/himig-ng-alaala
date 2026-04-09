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

class Config:
    # Enable debug mode (auto reload + error messages)
    DEBUG = True

    #App Settings
    CACHE_LIMIT = 1000
    LASTFM_RESULT_LIMIT = 100
