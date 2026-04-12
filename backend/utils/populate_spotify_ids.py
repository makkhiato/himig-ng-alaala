"""
PROJECT: Himig ng Alaala (Music Recommendation System)
FILE: populate_spotify_ids.py
PURPOSE: Data Enrichment & Cross-Platform Metadata Mapping

RESPONSIBILITIES:
1. SQL SCHEMA MANAGEMENT: Adds a 'spotify_id' column to the 'songs' table if not present.
2. API INTEGRATION: Authenticates and communicates with the Spotify Web API.
3. DATA MATCHING: Iterates through records to find the Track ID.
4. ATOMIC UPDATES: Persists IDs back into the SQLite database.
5. RATE LIMIT HANDLING: Uses built-in backoff logic and flags missing tracks
   to prevent redundant API calls on subsequent runs.
"""

import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# PRO-TIP: We configure spotipy to automatically handle 429 Rate Limits
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET),
    retries=5,               # Automatically retry up to 5 times if rate limited
    requests_timeout=10,     # Don't hang forever if the connection drops
    backoff_factor=1.0       # Exponential backoff (wait 1s, then 2s, then 4s, etc.)
)

DB_PATH = 'data/processed/music_data_final.db'

def populate_ids():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE songs ADD COLUMN spotify_id TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        print("Column 'spotify_id' already exists.")

    # Only fetch songs that have NEVER been searched (NULL)
    cursor.execute("SELECT artist, title FROM songs WHERE spotify_id IS NULL")
    songs = cursor.fetchall()

    if not songs:
        print("🎉 All songs have been processed! No API calls needed.")
        conn.close()
        return

    print(f"Searching for {len(songs)} remaining songs...")

    for artist, title in songs:
        query = f"track:{title} artist:{artist}"
        try:
            results = sp.search(q=query, limit=1, type='track')
            tracks = results['tracks']['items']

            if tracks:
                track_id = tracks[0]['id']
                cursor.execute("UPDATE songs SET spotify_id = ? WHERE artist = ? AND title = ?",
                               (track_id, artist, title))
                print(f"✅ Found: {title} by {artist}")
            else:
                # DATA SCIENTIST SHIELD: Mark as 'NOT_FOUND' so we don't query this again!
                cursor.execute("UPDATE songs SET spotify_id = 'NOT_FOUND' WHERE artist = ? AND title = ?",
                               (artist, title))
                print(f"❌ Not found: {title} by {artist} (Marked to skip future runs)")

            conn.commit()

            # A polite 0.5s delay keeps us at 120 requests per minute, well within safe limits.
            time.sleep(0.5)

        except spotipy.exceptions.SpotifyException as e:
            # If we hit a hard rate limit despite retries, save progress and exit cleanly
            if e.http_status == 429:
                print("\n🚨 CRITICAL RATE LIMIT HIT. Exiting to protect account. Try again later.")
                break
            else:
                print(f"⚠️ API Error searching {title}: {e}")
                time.sleep(2)
        except Exception as e:
            print(f"⚠️ Unexpected Error searching {title}: {e}")
            time.sleep(2)

    conn.close()
    print("\nBatch Complete! Progress has been saved to the database.")

if __name__ == "__main__":
    populate_ids()