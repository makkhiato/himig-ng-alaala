"""
A functional utility module to handle local data storage.

Responsibilities:
1. Read the music_data.json file
2. Search for a song in the file
3. Add or update the file and save it immediately
"""

import json
import os

# Get the directory where THIS script (cache_manager_1.py) is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Point to your new data location
# This ensures it always finds the file in backend/data/processed/ regardless of where you run it
FILE_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'music_data_normalized.json')

def load_cache():
    """Reads the JSON file from the backend directory."""
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Return empty list if file is empty or corrupted
            return []
    return []

def save_cache(cache_list):
    """Saves the list to music_data.json in the backend directory."""
    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(cache_list, f, indent=4)
    except IOError as e:
        print(f"Error saving to {FILE_PATH}: {e}")


def get_cached_song(cache_list, artist, title):
    """Finds a song in the list. Case-insensitive."""
    for song in cache_list:
        if (song.get('artist').lower() == artist.lower() and
                song.get('title').lower() == title.lower()):
            return song
    return None


def update_cache(cache_list, artist, title, new_data):
    """Updates the data dictionary for a song and saves to disk."""
    song = get_cached_song(cache_list, artist, title)

    if song:
        # Merges new data into existing song entry
        song.update(new_data)
    else:
        # Creates a new entry if the song wasn't found
        new_entry = {"artist": artist, "title": title}
        new_entry.update(new_data)
        cache_list.append(new_entry)

    # Save the updated list to the file immediately
    save_cache(cache_list)
    return cache_list


# =====================================================================
#                           TEST FUNCTION
# =====================================================================
def run_tests():
    print("--- STARTING CACHE MANAGER TESTS ---")

    # 1. Test load_cache (Create file if it doesn't exist)
    print("\nTest 1: Loading Cache...")
    data = load_cache()
    print(f"Current cache size: {len(data)} songs.")

    # 2. Test update_cache (Adding a new song)
    print("\nTest 2: Adding a new song (Chicosci - Diamond Shotgun)...")
    test_artist = "Chicosci"
    test_title = "Diamond Shotgun"
    test_data = {"soundcharts_uuid": "test-uuid-123"}

    updated_data = update_cache(data, test_artist, test_title, test_data)

    if any(s['title'] == test_title for s in updated_data):
        print("Success: Song added/updated in memory and saved to disk.")
    else:
        print("Fail: Song not found in updated data.")

    # 3. Test get_cached_song (Searching)
    print("\nTest 3: Searching for the song we just added...")
    found_song = get_cached_song(updated_data, "chicosci", "diamond shotgun")  # testing lowercase

    if found_song and found_song.get('soundcharts_uuid') == "test-uuid-123":
        print(f"Success: Found {found_song['artist']} - {found_song['title']} with correct UUID.")
    else:
        print("Fail: Could not retrieve the correct song from cache.")

    # 4. Test update_cache (Updating existing song with audio features)
    print("\nTest 4: Adding audio features to the same song...")
    audio_features = {"energy": 0.95, "tempo": 145}
    final_data = update_cache(updated_data, test_artist, test_title, audio_features)

    final_song = get_cached_song(final_data, test_artist, test_title)
    if final_song.get('energy') == 0.95 and final_song.get('soundcharts_uuid') == "test-uuid-123":
        print("Success: Existing entry successfully merged new data with old data.")
    else:
        print("Fail: Data was overwritten instead of merged.")

    print("\n--- ALL TESTS COMPLETED ---")
    print("Check 'music_data.json' in your backend folder to see the results.")