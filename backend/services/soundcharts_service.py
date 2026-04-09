"""
DOCUMENTATION: SOUNDCHARTS SERVICE (RAW API VERSION)
----------------------------------
PURPOSE:
Acquires UUIDs and Audio Features directly from the Soundcharts REST API.

RESPONSIBILITIES:
1. Direct API Calls: Uses 'requests' to avoid SDK-specific class errors.
2. Header Management: Manages App-ID and API-Key manually.
3. Path Handling: Dynamically finds the .env file in the backend root.
"""

import os
import time
import requests
from dotenv import load_dotenv
from pathlib import Path
from services import cache_manager as cm
from urllib.parse import quote

# 1. SETUP: Ensure .env is loaded correctly from the backend root
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

APP_ID = os.getenv("SOUNDCHARTS_APP_ID")
API_TOKEN = os.getenv("SOUNDCHARTS_TOKEN")

# Headers required by Soundcharts API
HEADERS = {
    "x-app-id": APP_ID,
    "x-api-key": API_TOKEN
}

SEARCH_URL = "https://customer.api.soundcharts.com/api/v2"
FEATURE_URL = "https://customer.api.soundcharts.com/api/v2.25"


def process_genre_batch(genre_name, song_list, mode="SEARCH"):
    music_data = cm.load_cache()
    print(f"\n--- [API MODE] Genre: {genre_name} | Mode: {mode} ---")

    for song in song_list:
        artist = song.get('artist')
        title = song.get('title')

        # Skip logic
        existing_entry = cm.get_cached_song(music_data, artist, title)
        if mode == "SEARCH" and existing_entry and 'uuid' in existing_entry:
            continue
        if mode == "FEATURES" and existing_entry and 'energy' in existing_entry:
            continue

        try:
            if mode == "SEARCH":
                # Step 1: Search for the song
                # Endpoint: /song/search/{term}
                search_term = f"{artist} {title}"
                encoded_term = quote(search_term)
                url = f"{SEARCH_URL}/song/search/{encoded_term}"

                response = requests.get(url, headers=HEADERS, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    if items:
                        # SMART MATCH: Try to find the item where creditName matches artist
                        # Otherwise, just take the first result.
                        best_match = next(
                            (item for item in items if artist.lower() in item.get('creditName', '').lower()),
                            items[0]
                        )
                        uuid = best_match.get('uuid')

                        music_data = cm.update_cache(music_data, artist, title, {"uuid": uuid, "genre": genre_name})
                        print(f"  [UUID] Found {uuid} for {title}")
                    else:
                        print(f"  [NOT FOUND] {title}")
                else:
                    print(f"  [API ERROR] {title}: Status {response.status_code}")

            elif mode == "FEATURES":
                # Step 2: Get metadata/features
                if not existing_entry or 'uuid' not in existing_entry:
                    continue

                uuid = existing_entry['uuid']
                url = f"{FEATURE_URL}/song/{uuid}"

                response = requests.get(url, headers=HEADERS, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    # Drill down into the 'object' then 'audio'
                    object_data = data.get('object', {})
                    audio = object_data.get('audio', {})

                    if audio:
                        features = {
                            "valence": audio.get('valence'),
                            "energy": audio.get('energy'),
                            "tempo": audio.get('tempo'),
                            "danceability": audio.get('danceability')
                        }
                        music_data = cm.update_cache(music_data, artist, title, features)
                        print(f"  [FEATURES] {title} synced.")
                    else:
                        print(f"  [NO AUDIO DATA] {title}")
                else:
                    print(f"  [API ERROR] {title}: Status {response.status_code}")

        except Exception as e:
            print(f"  [CRASH] {title}: {e}")

    print(f"\nFinished batch for {genre_name}.")