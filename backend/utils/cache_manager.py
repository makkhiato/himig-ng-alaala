"""
A database-backed utility module to handle local data storage for Himig ng Alaala.

Responsibilities:
1. Connect to himig_ng_alaala.db
2. Search for a song using SQL queries (O(1) search with indexing)
3. Add or update rows without rewriting the entire dataset
"""

import sqlite3
import os
from pathlib import Path
import pandas as pd

# Modern path handling
BASE_DIR = Path(__file__).parent.parent
# DB_PATH = BASE_DIR / 'data' / 'music_data_final.db'
DB_PATH = BASE_DIR / 'data' / 'processed' / 'test_music.db'

def get_connection():
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def get_cached_song(artist, title):
    """
    Finds a song in the database using SQL.
    Returns a dictionary of the song data or None if not found.
    """
    conn = get_connection()
    # This makes results accessible by column name like song['energy']
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM songs WHERE LOWER(artist) = LOWER(?) AND LOWER(title) = LOWER(?)"

    try:
        cursor.execute(query, (artist, title))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def save_or_update_song(artist, title, data):
    """
    Upserts (Update or Insert) a song into the database.
    This is much more efficient than rewriting a JSON file.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if song exists
    existing_song = get_cached_song(artist, title)

    if existing_song:
        # 1. Update existing row
        # Dynamically build the SET clause based on what's in 'data'
        columns = ", ".join([f"{key} = ?" for key in data.keys()])
        values = list(data.values()) + [artist, title]

        query = f"UPDATE songs SET {columns} WHERE LOWER(artist) = LOWER(?) AND LOWER(title) = LOWER(?)"
        cursor.execute(query, values)
    else:
        # 2. Insert new row
        # Ensure artist and title are part of the insert
        data['artist'] = artist
        data['title'] = title
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])

        query = f"INSERT INTO songs ({columns}) VALUES ({placeholders})"
        cursor.execute(query, list(data.values()))

    conn.commit()
    conn.close()


# =====================================================================
#                           REFACTORED TESTS
# =====================================================================
def run_tests():
    # --- SANDBOX SETUP ---
    # If the test DB doesn't have the table, let's create it using one row from our real data
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='songs';")

    if not cursor.fetchone():
        print("🛠️ Test table 'songs' not found. Initializing sandbox schema...")
        # Path to your REAL data to borrow the structure
        real_db = Path(__file__).parent.parent / 'data' / 'processed' / 'music_data_final.db'

        # Connect to real DB, grab 1 row, and push it to the test DB
        real_conn = sqlite3.connect(real_db)
        df_sample = pd.read_sql_query("SELECT * FROM songs LIMIT 1", real_conn)
        df_sample.to_sql('songs', conn, if_exists='replace', index=False)
        real_conn.close()
        print("✅ Sandbox initialized with real schema.")
    conn.close()

    print("--- STARTING SQL CACHE MANAGER TESTS ---")

    test_artist = "Chicosci"
    test_title = "Diamond Shotgun"

    # 1. Test Search
    print(f"\nTest 1: Searching for {test_artist}...")
    song = get_cached_song(test_artist, test_title)
    if song:
        print(f"Found existing song: {song['artist']} - {song['title']}")
    else:
        print("Song not in DB yet.")

    # 2. Test Upsert (Insert/Update)
    print(f"\nTest 2: Updating {test_title} with audio features...")
    features = {
        "uuid": "chicosci-001",
        "energy": 0.98,
        "tempo_normalized": 0.75,
        "genre": "opm"
    }
    save_or_update_song(test_artist, test_title, features)

    # 3. Verify
    verified = get_cached_song(test_artist, test_title)
    if verified and verified.get('energy') == 0.98:
        print(f"Success! {verified['title']} updated in the SQL database.")
    else:
        print("Fail: Database update failed.")

    print("\n--- ALL TESTS COMPLETED ---")


if __name__ == "__main__":
    run_tests()