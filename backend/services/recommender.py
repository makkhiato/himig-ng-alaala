import pandas as pd
import sqlite3
import json
from pathlib import Path
from sklearn.metrics.pairwise import euclidean_distances
import logging

logger = logging.getLogger(__name__)

# Path setup
BASE_DIR = Path(__file__).parent.parent  # This goes from 'services' up to 'backend'
DB_PATH = BASE_DIR / 'data' / 'processed' / 'music_data_final.db'


def get_recommendations(user_vector, user_genre):

    target_genre = user_genre.get('genre')

    feature_mapping = {
        'valence': user_vector['valence'],
        'energy': user_vector['energy'],
        'danceability': user_vector['danceability'],
        'tempo_normalized': user_vector['tempo']
    }

    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM songs WHERE LOWER(genre) = LOWER(?)"
    df_genre = pd.read_sql_query(query, conn, params=(target_genre,))
    conn.close()
    logger.info(f"Retrieved {len(df_genre)} songs from database for genre '{target_genre}'")

    if df_genre.empty:
        logger.warning(f"Zero songs found in database for genre: {target_genre}")
        return json.dumps({"error": f"No songs found for genre: {target_genre}"})

    features_list = list(feature_mapping.keys())
    df_genre = df_genre.dropna(subset=features_list)

    if df_genre.empty:
        logger.warning(f"Songs in database missing features")
        return json.dumps({"error": "Songs missing features"})

    song_vectors = df_genre[features_list].values
    user_vec = [list(feature_mapping.values())]

    distances = euclidean_distances(user_vec, song_vectors)[0]

    max_distance = 2.0
    true_percentage = (1 - (distances / max_distance)) * 100

    df_genre['similarity_percentage'] = true_percentage.round(2)
    df_genre['similarity_percentage'] = df_genre['similarity_percentage'].apply(lambda x: max(45.0, x))

    # ✅ THIS MUST EXIST
    top_5 = df_genre.sort_values(by='similarity_percentage', ascending=False).head(5)

    # ✅ NEW FIXED FORMAT
    recommendations_list = []

    for _, row in top_5.iterrows():
        spotify_id = row.get('spotify_id', '')

        recommendations_list.append({
            "artist": row['artist'],
            "title": row['title'],
            "match": row['similarity_percentage'],
            "genre": row['genre'],
            "spotify_id": spotify_id,
            "spotify_url": f"https://open.spotify.com/track/{spotify_id}" if spotify_id else "",
            "spotify_uri": f"spotify:track:{spotify_id}" if spotify_id else ""
        })

    song_summary = [f"{Song['title']} ({Song['match']}%)" for Song in recommendations_list]
    songs_string = ", ".join(song_summary)
    logger.info(f"Top 5 for '{target_genre}': {songs_string}")

    # ✅ RETURN INSIDE FUNCTION
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