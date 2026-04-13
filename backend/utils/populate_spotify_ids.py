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
from collections import defaultdict
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
            time.sleep(2)

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


def get_valid_tracks_by_genre():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SQL Query: Get everything that actually has a real Spotify ID
        query = """
            SELECT genre, artist, title, spotify_id 
            FROM songs 
            WHERE spotify_id IS NOT NULL 
              AND spotify_id != 'NOT_FOUND'
            ORDER BY genre, artist
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Grouping the results using a dictionary
        songs_by_genre = defaultdict(list)
        for genre, artist, title, spotify_id in results:
            # Handle cases where genre might be empty/null
            safe_genre = genre if genre else "Unknown Genre"
            songs_by_genre[safe_genre].append({
                "artist": artist,
                "title": title,
                "spotify_id": spotify_id
            })

        # --- Output the Analysis ---
        print("\n📊 --- VALID SPOTIFY TRACKS PER GENRE --- 📊\n")

        total_valid_songs = 0

        for genre, track_list in songs_by_genre.items():
            count = len(track_list)
            total_valid_songs += count
            print(f"🎵 {genre.upper()}: {count} tracks")

            # Print a quick sample of up to 3 songs per genre to verify
            sample_size = min(3, count)
            for i in range(sample_size):
                song = track_list[i]
                print(f"    - {song['title']} by {song['artist']} ({song['spotify_id']})")
            if count > 3:
                print(f"    ... and {count - 3} more.")
            print("-" * 40)

        print(f"\n✅ Total valid songs across all genres: {total_valid_songs}")

        conn.close()

        # Returns the dictionary in case you want to import this function elsewhere
        return dict(songs_by_genre)

    except sqlite3.Error as e:
        print(f"⚠️ Database error: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")


def get_missing_tracks_by_genre():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SQL Query: Get everything flagged as 'NOT_FOUND'
        query = """
            SELECT genre, artist, title 
            FROM songs 
            WHERE spotify_id = 'NOT_FOUND'
            ORDER BY genre, artist
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Grouping the results using a dictionary
        missing_by_genre = defaultdict(list)
        for genre, artist, title in results:
            safe_genre = genre if genre else "Unknown Genre"
            missing_by_genre[safe_genre].append({
                "artist": artist,
                "title": title
            })

        # --- Output the Analysis ---
        print("\n⚠️ --- 'NOT FOUND' TRACKS PER GENRE --- ⚠️\n")

        total_missing = 0

        if not results:
            print("🎉 Amazing! There are no 'NOT_FOUND' tracks in your database.")
        else:
            for genre, track_list in missing_by_genre.items():
                count = len(track_list)
                total_missing += count
                print(f"🎵 {genre.upper()}: {count} tracks missing")

                # Print all missing tracks so you can review them
                for song in track_list:
                    print(f"    ❌ {song['title']} by {song['artist']}")
                print("-" * 50)

            print(f"\nTotal 'NOT_FOUND' songs across all genres: {total_missing}")

        conn.close()

    except sqlite3.Error as e:
        print(f"⚠️ Database error: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")


def delete_missing_tracks():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. Check how many we are about to delete
        cursor.execute("SELECT COUNT(*) FROM songs WHERE spotify_id = 'NOT_FOUND'")
        songs_to_delete = cursor.fetchone()[0]

        if songs_to_delete == 0:
            print("🎉 No 'NOT_FOUND' songs detected. Your database is already clean!")
            conn.close()
            return

        print(f"⚠️ Found {songs_to_delete} unplayable tracks.")
        print("🗑️ Deleting from database...")

        # 2. Execute the DELETE command
        cursor.execute("DELETE FROM songs WHERE spotify_id = 'NOT_FOUND'")

        # 3. COMMIT is required to save changes when modifying a database!
        conn.commit()

        # 4. Check how many songs are left overall
        cursor.execute("SELECT COUNT(*) FROM songs")
        remaining_songs = cursor.fetchone()[0]

        print(f"✅ Success! Removed {songs_to_delete} tracks.")
        print(f"🎵 Your clean dataset now has {remaining_songs} perfectly playable songs.")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    delete_missing_tracks()