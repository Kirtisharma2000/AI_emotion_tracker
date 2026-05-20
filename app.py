from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from scipy.sparse import csr_matrix


with open("models/emotion_model.pkl", "rb") as f:
    state_model = pickle.load(f)

with open("models/intensity_model.pkl", "rb") as f:
    intensity_model = pickle.load(f)

with open("models/tfidf.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

app = Flask(__name__)

def preprocess_input(journal_text, metadata):

    text_features = tfidf_vectorizer.transform([journal_text])

    input_data = {

        "sleep_hours": metadata.get("sleep_hours", 6),
        "energy_level": metadata.get("energy_level", 3),
        "stress_level": metadata.get("stress_level", 3),
        "duration_min": metadata.get("duration_min", 10),
        "text_length": len(journal_text),
        "word_count": len(journal_text.split()),
        "ambience_type": metadata.get("ambience_type", "quiet"),
        "time_of_day": metadata.get("time_of_day", "morning"),
        "previous_day_mood": metadata.get("previous_day_mood", "neutral"),
        "face_emotion_hint": metadata.get("face_emotion_hint", "neutral"),
        "reflection_quality": metadata.get("reflection_quality", "medium")
    }

    meta_df = pd.DataFrame([input_data])

    meta_df = pd.get_dummies(meta_df)

    meta_df = meta_df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    meta_features = csr_matrix(meta_df.values)

    X_input = hstack([text_features, meta_features])

    return X_input

def decision_layer(state, intensity, metadata):

    stress = metadata.get("stress_level", 3)
    energy = metadata.get("energy_level", 3)
    time_of_day = metadata.get("time_of_day", "morning")

    if intensity >= 4 or stress >= 4:
        what_to_do = "deep_work" if energy >= 3 else "rest"
    elif intensity <= 2:
        what_to_do = "journaling"
    else:
        what_to_do = "box_breathing"

    if time_of_day in ["morning", "afternoon"]:
        when_to_do = "now" if stress >= 3 else "within_15_min"
    else:
        when_to_do = "later_today"

    return what_to_do, when_to_do


@app.route("/", methods=["GET", "POST"])
def predict():

    if request.method == "GET":
        return render_template("index.html")

    try:

        data = request.get_json()

        print("Incoming Data:", data)

        journal_text = data.get("journal_text", "")
        metadata = data.get("metadata", {})

        X_input = preprocess_input(journal_text, metadata)

        print("Input Shape:", X_input.shape)

        predicted_state = state_model.predict(X_input)[0]

        state_proba = state_model.predict_proba(X_input).max()

        predicted_intensity = intensity_model.predict(X_input)[0]

        uncertain_flag = 1 if state_proba < 0.6 else 0

        what_to_do, when_to_do = decision_layer(
            predicted_state,
            predicted_intensity,
            metadata
        )

        response = {
            "predicted_state": str(predicted_state),
            "predicted_intensity": int(predicted_intensity),
            "confidence": float(state_proba),
            "uncertain_flag": uncertain_flag,
            "what_to_do": what_to_do,
            "when_to_do": when_to_do,
        }

        return jsonify(response)

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)







