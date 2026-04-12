"""
This file handles the API endpoint for handling survey submissions

Responsibilities:
- Receive survey data from frontend (JSON)
- Validate incoming request
- Extract relevant fields (answers, genre)
- Call vibe_mapper.py to convert answers into a target vector
- Return the processed vector to the frontend

INPUT: Frontend -> Survey answers in JSON format
OUTPUT: Recommended song title and artist in JSON format -> Frontend
"""

from flask import Blueprint, request, jsonify
from utils.vibe_mapper import map_to_vector
from services.recommender import get_recommendations
import json

survey_bp = Blueprint("survey", __name__)


@survey_bp.route("/process-survey", methods=["POST"])
def process_survey():
    try:
        # 1. Get JSON data from request
        data = request.get_json()

        # 2. Validate if frontend sent the survey answers
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # 3. Extract answers and genre
        answers = data.get("answers", {})
        raw_genre = data.get("genre", "")

        if isinstance(raw_genre, dict):
            genre_value = raw_genre.get("genre", "")
        else:
            genre_value = raw_genre

        # Normalize genre values from frontend
        genre_map = {
            "R&B": "rnb",
            "RnB": "rnb",
            "Hip-Hop": "hiphop",
            "HipHop": "hiphop",
            "K-Pop": "kpop",
            "KPop": "kpop",
            "Pop": "pop",
            "OPM": "opm",
            "Rock": "rock",
            "Metal": "metal",
            "Indie": "indie",
            "Jazz": "jazz",
            "Acoustic": "acoustic"
        }

        normalized_genre = genre_map.get(genre_value, str(genre_value).lower())
        genre_dict = {"genre": normalized_genre}

        # 4. Logic: Map survey to vector -> Get recommendations
        user_vector = map_to_vector(answers)
        recommendations = get_recommendations(user_vector, genre_dict)

        # If recommender returns a JSON string, parse it
        if isinstance(recommendations, str):
            recommendations_list = json.loads(recommendations)
        else:
            recommendations_list = recommendations

        # Check for errors returned by recommender logic
        if isinstance(recommendations_list, dict) and "error" in recommendations_list:
            return jsonify(recommendations_list), 404

        return jsonify({
            "status": "success",
            "results": recommendations_list
        }), 200

    except Exception as e:
        print("Error processing the survey:", e)
        return jsonify({
            "error": "Internal service error",
            "details": str(e)
        }), 500