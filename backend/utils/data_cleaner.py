import pandas as pd
import json

def clean_music_data(file_path):
    # 1. Load the data
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(data)
    initial_count = len(df)
    print(f"Initial record count: {initial_count}")

    # 2. Remove Exact Duplicates
    # This checks for rows where every single column is identical
    df = df.drop_duplicates()

    # 3. Handle Missing UUIDs
    # Removes rows where 'uuid' is None, NaN, or an empty string
    df = df.dropna(subset=['uuid'])
    df = df[df['uuid'] != ""]

    # 4. Handle Missing Features
    # You can specify critical columns like 'energy', 'tempo', or 'danceability'
    # For now, let's drop rows that are missing any data in your feature columns
    critical_features = ['artist', 'title', 'genre']  # Add your specific vibe features here
    df = df.dropna(subset=critical_features)

    # 5. Final Count & Stats
    final_count = len(df)
    removed_count = initial_count - final_count

    print(f"Cleaned record count: {final_count}")
    print(f"Removed {removed_count} problematic or duplicate records.")

    # 6. Count of songs per genre
    genre_counts = df['genre'].value_counts()
    print("\n--- Songs per Genre ---")
    print(genre_counts)

    # 7. Save the cleaned data back to JSON
    df.to_json('music_data_cleaned.json', orient='records', indent=4)
    print("\nCleaned data saved to 'music_data_cleaned.json'")


if __name__ == "__main__":
    clean_music_data('music_data.json')