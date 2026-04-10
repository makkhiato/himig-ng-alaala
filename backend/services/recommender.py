import pandas as pd
import sqlite3
import json
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

# Path setup
BASE_DIR = Path(__file__).parent.parent  # This goes from 'services' up to 'backend'
DB_PATH = BASE_DIR / 'data' / 'processed' / 'music_data_final.db'


def get_recommendations(user_vector, user_genre):
    """
    Args:
        user_vector (dict): {'valence': 0.5, 'energy': 0.5, 'tempo': 0.5, 'danceability': 0.5}
        user_genre (dict): {'genre': 'pop'}
    """

    # 1. Extract inputs
    target_genre = user_genre.get('genre')

    # 2. Define the keys we are using for the math
    # NOTE: I renamed 'tempo' to 'tempo_normalized' to match your SQL column name
    feature_mapping = {
        'valence': user_vector['valence'],
        'energy': user_vector['energy'],
        'danceability': user_vector['danceability'],
        'tempo_normalized': user_vector['tempo']  # Mapping user 'tempo' to DB 'tempo_normalized'
    }

    # 3. Pull data from SQL
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM songs WHERE LOWER(genre) = LOWER(?)"
    df_genre = pd.read_sql_query(query, conn, params=(target_genre,))
    conn.close()

    if df_genre.empty:
        return f"No songs found for genre: {target_genre}"

    # Drop any rows that have missing values in our features so the math doesn't break
    features_list = list(feature_mapping.keys())
    df_genre = df_genre.dropna(subset=features_list)

    # Also, double check if df_genre is still not empty after dropping NaNs
    if df_genre.empty:
        return "Found songs, but they are missing the required audio features."

    # 4. Prepare vectors for Cosine Similarity
    # We grab the keys from our mapping to ensure the order is identical
    features_list = list(feature_mapping.keys())

    # Song vectors from DB (filtered by the same features)
    song_vectors = df_genre[features_list].values

    # User vector from dict values
    user_vector = [list(feature_mapping.values())]

    # 5. Calculate Similarity
    # result is a list of scores between 0 and 1
    similarities = cosine_similarity(user_vector, song_vectors)[0]

    # 6. Formatting Results
    df_genre['similarity_percentage'] = (similarities * 100).round(2)

    # Sort and pick top 5
    top_5 = df_genre.sort_values(by='similarity_percentage', ascending=False).head(5)

    result_columns = ['artist', 'title', 'similarity_percentage', 'genre']
    recommendations_list = top_5[result_columns].to_dict(orient='records')

    # Return as a JSON string
    return json.dumps(recommendations_list, indent=4, ensure_ascii=False)


# =====================================================================
#                           PROTOTYPE TEST
# =====================================================================
if __name__ == "__main__":
    # 1. Setup Test Data
    my_vibe = {"valence": 0.8, "energy": 0.9, "tempo": 0.85, "danceability": 0.9}
    my_genre = {"genre": "rnb"}

    # 2. Get the JSON Response (This simulates what your Frontend will receive)
    json_response = get_recommendations(my_vibe, my_genre)

    # 3. Print the RAW JSON (The "API" View)
    print("--- RAW JSON RESPONSE ---")
    print(json_response)
    print("\n" + "=" * 50 + "\n")

    # 4. Print the Formatted View (The "Human" View)
    print(f"--- Top 5 Recommendations for {my_genre['genre'].upper()} ---")

    # We parse the JSON back to a list to iterate over it
    data = json.loads(json_response)

    if isinstance(data, list):
        for song in data:
            print(f"[{song['similarity_percentage']}% Match] {song['artist']} - {song['title']} ({song['genre']})")
    else:
        # This handles the case where the JSON returned an {"error": "..."} object
        print(f"Error: {data.get('error')}")