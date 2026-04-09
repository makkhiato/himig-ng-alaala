"""
This script acts as the 'Initial Seeder' for the music database. It pulls
popular tracks from Last.fm based on specific genre tags to build the
foundation of the music_data.json file.

Responsibilities:
1. API Extraction: Fetches the top 100 tracks for a given genre tag.
2. Data Seeding: Integrates with cache_manager.py to save the artist,
   title, and genre locally.
3. Formatting: Cleans the Last.fm response into a flat structure ready
   for the Soundcharts Phase.

INPUT: genre (str) -> songs
OUTPUT: Initialized entries -> music_data.json
"""

import requests
import os
from dotenv import load_dotenv
from services import cache_manager as cm

load_dotenv()

CLIENT_KEY = os.getenv("LASTFM_API_KEY")
CLIENT_SECRET = os.getenv("LASTFM_SHARED_SECRET")

BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def seed_genre_from_lastfm(genre_query):
    """
    Fetches top tracks for a genre and seeds them into the local cache.
    """
    # 1. Identify application and setup params
    headers = {'User-Agent': 'PLM_Music_Booth_Project/1.0'}

    params = {
        "method": "tag.gettoptracks",
        "tag": genre_query,
        "api_key": CLIENT_KEY,
        "format": "json",
        "limit": 100  # We want a full batch of 100 for our booth dataset
    }

    try:
        # 2. Load the existing cache list
        music_cache = cm.load_cache()

        print(f"--- Seeding Last.fm data for: {genre_query} ---")
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"FAILED: Last.fm API returned status {response.status_code}")
            return

        # Extract the track list from the JSON structure
        # Path: toptracks -> track
        data = response.json()
        tracks = data.get('tracks', {}).get('track', [])

        if not tracks:
            print(f"NOTICE: No tracks found for the tag '{genre_query}'")
            return []

        # 3. Loop through tracks and update the cache
        for t in tracks:
            artist_name = t.get('artist', {}).get('name')
            song_title = t.get('name')

            # We only save the basics here. Soundcharts will fill the rest later.
            # cm.update_cache automatically handles duplicates and saves to disk.
            music_cache = cm.update_cache(
                music_cache,
                artist_name,
             song_title,
                {"genre": genre_query}
            )

            print(f"SUCCESS: Seeded {len(tracks)} tracks for {genre_query}.")

    except Exception as e:
        print(f"UNEXPECTED ERROR in lastfm_service: {e}")