import pandas as pd
import sqlite3
from pathlib import Path


def migrate():
    # 1. Setup Paths
    # Since you are in 'backend', Path.cwd() points to 'backend'
    base_path = Path.cwd()
    json_input = base_path / 'data' / 'processed' / 'music_data_normalized.json'
    db_output = base_path / 'data' / 'processed' / 'music_data_final.db'

    # Ensure the directory exists just in case
    db_output.parent.mkdir(parents=True, exist_ok=True)

    # 2. Load the cleaned JSON
    if not json_input.exists():
        print(f"❌ Error: Could not find {json_input}")
        return

    print(f"📂 Loading data from {json_input.name}...")
    df = pd.read_json(json_input)

    # 3. Connect to SQLite
    print(f"🔗 Creating database at {db_output}...")
    conn = sqlite3.connect(db_output)

    try:
        # 4. The Migration
        print("🚀 Migrating records to SQL table 'songs'...")
        # if_exists='replace' is best for the first migration to ensure a clean schema
        df.to_sql('songs', conn, if_exists='replace', index=False)

        # 5. The 'Show Off' Index
        # This makes searching by uuid, artist, or title significantly faster
        print("⚡ Adding database indexes for performance...")
        conn.execute("CREATE INDEX idx_uuid ON songs(uuid);")
        conn.execute("CREATE INDEX idx_artist_title ON songs(artist, title);")

        print(f"✅ Success! Database is ready at: {db_output}")

    except Exception as e:
        print(f"❌ Migration failed: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    migrate()