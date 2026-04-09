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

survey_bp = Blueprint("survey",__name__)

@survey_bp.route("/process-survey", methods = ["POST"])
def process_survey():
    try:
        #Get JSON Data from request
        data = request.json

        #Validating if Frontend sent the survey answers
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        #Extract answers and genre
        answers = data.get("answers", {})
        genre = data.get("genre", "pop")

        return jsonify({"message": "Survey processed successfully"}), 200

    except Exception as e:
        #Catch unexpected errors to avoid crashing the app
        print("Error processing the survey: ", e)
        return jsonify({"error": "Internal service error"}), 500

def recommend_song(answers, genre):
    pass
