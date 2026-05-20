1. Setup Instruction

   Create a project folder on our computer
   Place all files inside the folder
    - train_data.csv 
    - test_data.csv


2. Approach

   1) The system is a hybrid ML + rule-based pipeline:
   - Emotional Understanding
   - Predicts emotional_state and intensity from:
   - Journal text
   - Metadata: sleep, stress, energy, time-of-day, previous mood

   2) Decision Engine
   - Determines what to do (e.g., breathing, journaling, deep work, rest)
   - Determines when to do it (e.g., now, within 15 min, later today)
   - Inputs: predicted state, intensity, stress, energy, time-of-day

   3)Uncertainty Modeling
   - Confidence score (0–1)
   - uncertain_flag if confidence < 0.6


3. Feature Engineering

   1) Text Features
   - Journal text → TF-IDF vectors
   - Captures keywords and emotional tone

   2) Metadata Features
   - Numerical: sleep_hours, energy_level, stress_level, duration_min 
   - Categorical: time_of_day, previous_day_mood, ambience_type
   - Face hints: face_emotion_hint

   3)Combining Features
   - Text + metadata → final feature set for ML model
   - Metadata corrects ambiguous or short text


4. Model Choice

   1) Emotional State Prediction
   - LogisticRegressor
   - Robust to structured + sparse features

   2) Intensity Prediction
   - RandomForestClassifier (ordinal classification 1–5)

   3) Decision Engine
   - Rule-based using predicted state, intensity, and metadata
   
   4) Uncertainty Modeling
   - Confidence based on model probabilities

   Ablation Study: Text-only vs Text + Metadata → combined model is more robust
