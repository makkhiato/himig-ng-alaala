"""
This file handles the API endpoint for handling survey submissions

Responsibilities:
- Receive survey data from frontend (JSON)
- Validate incoming request
- Extract relevant fields (answers, genre)
- Call vibe_mapper.py to convert answers into a target vector
- Return the processed vector to the frontend

INPUT: Frontend -> Survey answers in JSON Format
OUTPUT: Recommended Song Title and Artist in JSON Format -> Frontend
"""

from flask import Blueprint, request, jsonify
from backend.utils.vibe_mapper import map_to_vector
from backend.services.recommender import get_recommendations
import json


survey_bp = Blueprint("survey",__name__)

@survey_bp.route("/process-survey", methods = ["POST"])
def process_survey():
    try:
        # 1. Get JSON Data from request
        data = request.json

        # 2. Validating if Frontend sent the survey answers
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # 3. Extract answers and genre
        answers = data.get("answers", {})
        raw_genre = data.get("genre", {})
        genre_dict = {"genre": raw_genre} if isinstance(raw_genre, str) else raw_genre

        if genre_dict["genre"] == "R&B":
            genre_dict.update({"genre": "rnb"})
        elif genre_dict["genre"] == "Hip-Hop":
            genre_dict.update({"genre": "hiphop"})
        elif genre_dict["genre"] == "K-Pop":
            genre_dict.update({"genre": "kpop"})

        # 4. Logic: Map survey to Vector -> Get Recommendations
        user_vector = map_to_vector(answers)
        recommendations = get_recommendations(user_vector, genre_dict)

        # We parse the string back to a Python list so jsonify sends it properly
        recommendations_list = json.loads(recommendations)

        # Check for errors returned by the recommender logic
        if isinstance(recommendations_list, dict) and "error" in recommendations_list:
            return jsonify(recommendations_list), 404

        return jsonify({
            "status": "success",
            "results": recommendations_list
        }), 200

    except Exception as e:
        #Catch unexpected errors to avoid crashing the app
        print("Error processing the survey: ", e)
        return jsonify({"error": "Internal service error", "details": str(e)}), 500