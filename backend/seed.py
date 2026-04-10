from services.lastfm_service import seed_genre_from_lastfm
from services.soundcharts_service import process_genre_batch
from backend.utils import cache_manager as cm


def run_pilot():
    print("🚀 STARTING PILOT RUN: acoustic GENRE")

    # STEP 1: Seed from Last.fm
    # This creates the entries in music_data.json
    print("\n[Step 1/3] Seeding 100 acoustic songs from Last.fm...")
    seed_genre_from_lastfm("acoustic")

    # Load the data we just seeded to pass into Soundcharts
    music_data = cm.load_cache()
    acoustic_songs = [s for s in music_data if s.get('genre') == 'acoustic']

    # STEP 2: Phase 1 - Search (UUIDs)
    # Ensure your .env has ACCOUNT A credentials
    print("\n[Step 2/3] Fetching UUIDs from Soundcharts (Account A)...")
    process_genre_batch("acoustic", acoustic_songs, mode="SEARCH")

    # STEP 3: Phase 2 - Features (Audio Metadata)
    # IMPORTANT: In a real run, you'd swap .env to ACCOUNT B here.
    # For a pilot of 100 songs, you can use the same account if you have quota.
    print("\n[Step 3/3] Fetching Audio Features from Soundcharts (Account B)...")
    # Re-fetch the list to ensure we have the new UUIDs in memory
    music_data = cm.load_cache()
    acoustic_songs_with_uuids = [s for s in music_data if s.get('genre') == 'acoustic']
    process_genre_batch("acoustic", acoustic_songs_with_uuids, mode="FEATURES")

    print("\n✅ PILOT RUN COMPLETE!")
    print("Check 'music_data.json' to see if the acoustic songs have energy, tempo, and valence.")

if __name__ == "__main__":
    run_pilot()