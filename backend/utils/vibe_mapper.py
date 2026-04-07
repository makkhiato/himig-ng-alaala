"""
This file converts raw survey answers into numerical target vectors used for song recommendations.

Responsibilities:
- Interpret user answers (qualitative → quantitative)
- Map them into 4 main features:
    - valence (happy <-> sad)
    - energy (intensity)
    - tempo (speed)
    - danceability (movement tendency)

These vectors will later be used to compare against song features
using similarity scoring (Euclidean distance).

INPUT: survey_routes.recommend_song -> Survey answers in JSON Format (except genre)
OUTPUT: Dictionary of vectors -> survey_routes.recommend_song
"""

def normalize(vectors):

    # Rounds the vectors to one decimal place and ensure they are: 0.0 <= vector <= 1
    for vector in vectors.keys():
        vectors[vector] = round(vectors[vector], 2)
        vectors[vector] = max(0, min(1, vectors[vector]))

    return vectors


def map_to_vector(answers):
    vector = {
        "valence": 0.5,
        "energy": 0.5,
        "tempo": 0.5,
        "danceability": 0.5
    }

    #VALENCE vector
    answer = answers.get("instrument")
    if answer == "Electric Guitar":
        vector["valence"] += 0.2
    elif answer == "Drums":
        vector["valence"] += 0.1
    elif answer == "Saxophone":
        vector["valence"] -= 0.1
    elif answer == "Piano":
        vector["valence"] -= 0.2

    answer = answers.get("life_scene")
    if answer == "A happy montage (everything is going right)":
        vector["valence"] += 0.2
    elif answer == "A calm “in-between” scene":
        vector["valence"] += 0.1
    elif answer == "The emotional climax":
        vector["valence"] -= 0.1
    elif answer == "A sad, reflective moment":
        vector["valence"] -= 0.2

    answer = answers.get("cant_sleep")
    if answer == "Something upbeat to distract yourself":
        vector["valence"] += 0.2
    elif answer == "Soft chill music":
        vector["valence"] += 0.1
    elif answer == "Ambient and instrumental":
        vector["valence"] -= 0.1
    elif answer == "Sad songs that match your mood":
        vector["valence"] -= 0.2

    answer = answers.get("music_era")
    if answer == "1980s":
        vector["valence"] += 0.2
    elif answer == "2000s":
        vector["valence"] += 0.1
    elif answer == "1990s":
        vector["valence"] -= 0.1
    elif answer == "2010s":
        vector["valence"] -= 0.2

    answer = answers.get("weather")
    if answer == "Sunny":
        vector["valence"] += 0.2
    elif answer == "Partly sunny":
        vector["valence"] += 0.1
    elif answer == "Cloudy":
        vector["valence"] -= 0.1
    elif answer == "Rainy":
        vector["valence"] -= 0.2

    answer = answers.get("roadtrip_vibe")
    if answer == "Singing and dancing in your seat":
        vector["valence"] += 0.2
    elif answer == "Vibing and tapping along":
        vector["valence"] += 0.1
    elif answer == "Relaxed, just enjoying":
        vector["valence"] -= 0.1
    elif answer == "Quiet and not reacting much":
        vector["valence"] -= 0.2

    #ENERGY vector
    answer = answers.get("social_battery")
    if answer == "100%":
        vector["energy"] += 0.2
    elif answer == "75%":
        vector["energy"] += 0.1
    elif answer == "50%":
        vector["energy"] -= 0.1
    elif answer == "25%":
        vector["energy"] -= 0.2

    answer = answers.get("stress_response")
    if answer == "Blast loud music to release everything":
        vector["energy"] += 0.2
    elif answer == "Play something groovy and distracting":
        vector["energy"] += 0.1
    elif answer == "Lie down with soft background music":
        vector["energy"] -= 0.1
    elif answer == "Sit in silence":
        vector["energy"] -= 0.2

    answer = answers.get("aux_control")
    if answer == "Something that makes EVERYONE jump":
        vector["energy"] += 0.2
    elif answer == "A catchy beat people can groove to":
        vector["energy"] += 0.1
    elif answer == "Chill vibes for background mood":
        vector["energy"] -= 0.1
    elif answer == "Something lowkey… not trying to stand out":
        vector["energy"] -= 0.2

    answer = answers.get("cant_sleep")
    if answer == "Something upbeat to distract yourself":
        vector["energy"] += 0.2
    elif answer == "Soft chill music":
        vector["energy"] += 0.1
    elif answer == "Ambient and instrumental":
        vector["energy"] -= 0.1
    elif answer == "Sad songs that match your mood":
        vector["energy"] -= 0.2

    answer = answers.get("music_era")
    if answer == "2000s":
        vector["energy"] += 0.2
    elif answer == "1980s":
        vector["energy"] += 0.1
    elif answer == "2010s":
        vector["energy"] -= 0.1
    elif answer == "1990s":
        vector["energy"] -= 0.2

    answer = answers.get("morning_routine")
    if answer == "Sprint through a workout":
        vector["energy"] += 0.2
    elif answer == "Do a moderate routine":
        vector["energy"] += 0.1
    elif answer == "Stretch slowly or meditate":
        vector["energy"] -= 0.1
    elif answer == "Stay in bed scrolling":
        vector["energy"] -= 0.2

    #TEMPO vector
    answer = answers.get("stress_response")
    if answer == "Blast loud music to release everything":
        vector["tempo"] += 0.2
    elif answer == "Play something groovy and distracting":
        vector["tempo"] += 0.1
    elif answer == "Lie down with soft background music":
        vector["tempo"] -= 0.1
    elif answer == "Sit in silence":
        vector["tempo"] -= 0.2

    answer = answers.get("cant_sleep")
    if answer == "Something upbeat to distract yourself":
        vector["tempo"] += 0.2
    elif answer == "Soft chill music":
        vector["tempo"] += 0.1
    elif answer == "Ambient and instrumental":
        vector["tempo"] -= 0.1
    elif answer == "Sad songs that match your mood":
        vector["tempo"] -= 0.2

    answer = answers.get("game_pace")
    if answer == "Fast-paced action, no breaks":
        vector["tempo"] += 0.2
    elif answer == "Balanced gameplay":
        vector["tempo"] += 0.1
    elif answer == "Slow and strategic":
        vector["tempo"] -= 0.1
    elif answer == "Something super chill":
        vector["tempo"] -= 0.2

    answer = answers.get("walking_pace")
    if answer == "Speed walking / almost running":
        vector["tempo"] += 0.2
    elif answer == "Walking fast but controlled":
        vector["tempo"] += 0.1
    elif answer == "Still walking normally":
        vector["tempo"] -= 0.1
    elif answer == "Accepting your fate, slow walk":
        vector["tempo"] -= 0.2

    answer = answers.get("music_era")
    if answer == "2010s":
        vector["tempo"] += 0.2
    elif answer == "1990s":
        vector["tempo"] += 0.1
    elif answer == "2000s":
        vector["tempo"] -= 0.1
    elif answer == "1980s":
        vector["tempo"] -= 0.2

    answer = answers.get("morning_routine")
    if answer == "Sprint through a workout":
        vector["tempo"] += 0.2
    elif answer == "Do a moderate routine":
        vector["tempo"] += 0.1
    elif answer == "Stretch slowly or meditate":
        vector["tempo"] -= 0.1
    elif answer == "Stay in bed scrolling":
        vector["tempo"] -= 0.2

    #DANCEABILITY vector
    answer = answers.get("social_battery")
    if answer == "100%":
        vector["danceability"] += 0.2
    elif answer == "75%":
        vector["danceability"] += 0.1
    elif answer == "50%":
        vector["danceability"] -= 0.1
    elif answer == "25%":
        vector["danceability"] -= 0.2

    answer = answers.get("aux_control")
    if answer == "Something that makes EVERYONE jump":
        vector["danceability"] += 0.2
    elif answer == "A catchy beat people can groove to":
        vector["danceability"] += 0.1
    elif answer == "Chill vibes for background mood":
        vector["danceability"] -= 0.1
    elif answer == "Something lowkey… not trying to stand out":
        vector["danceability"] -= 0.2

    answer = answers.get("beat_reaction")
    if answer == "Instantly start dancing":
        vector["danceability"] += 0.2
    elif answer == "Nod your head / groove a little":
        vector["danceability"] += 0.1
    elif answer == "Just listen and vibe":
        vector["danceability"] -= 0.1
    elif answer == "Stay completely still":
        vector["danceability"] -= 0.2

    answer = answers.get("music_era")
    if answer == "1990s":
        vector["danceability"] += 0.2
    elif answer == "2010s":
        vector["danceability"] += 0.1
    elif answer == "1980s":
        vector["danceability"] -= 0.1
    elif answer == "2000s":
        vector["danceability"] -= 0.2

    answer = answers.get("tiktok_reaction")
    if answer == "Learn the dance":
        vector["danceability"] += 0.2
    elif answer == "Try a little":
        vector["danceability"] += 0.1
    elif answer == "Just watching it":
        vector["danceability"] -= 0.1
    elif answer == "Ignore":
        vector["danceability"] -= 0.2

    answer = answers.get("roadtrip_vibe")
    if answer == "Singing and dancing in your seat":
        vector["danceability"] += 0.2
    elif answer == "Vibing and tapping along":
        vector["danceability"] += 0.1
    elif answer == "Relaxed, just enjoying":
        vector["danceability"] -= 0.1
    elif answer == "Quiet and not reacting much":
        vector["danceability"] -= 0.2

    vector = normalize(vector)

    return vector