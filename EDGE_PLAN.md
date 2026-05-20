1. Deployment Approach (Edge / Local Device)

    The system is designed to run entirely locally, including mobile or desktop devices, without cloud APIs.

    Pipeline
    1) Preprocessing
    - Clean and normalize journal text
    - Handle missing metadata with default values
    2) Feature Extraction
    - TF-IDF vectorization for text
    - Encode metadata features (numerical + categorical)
    3) Prediction
    - Load trained ML models: emotion_model.pkl & intensity_model.pkl
    - Predict emotional_state and intensity
    4) Decision Layer
    - Rule-based logic for:
      What to do (e.g., journaling, breathing, deep work, rest)
      When to do it (now, within 15 min, later today)
    5) Uncertainty Handling
    - Compute confidence from model probabilities
    - Trigger uncertain_flag if confidence < 0.6
    - Adjust recommendations accordingly


2. Optimizations for Edge Devices

    1) Model Size
    - Reduce TF-IDF features to 1,000–3,000 words
    - Use lightweight RandomForest or XGBoost models
    - Store models in .pkl files (small disk footprint)
    2) Latency
    - Preload models in memory
    - Use sparse matrices for TF-IDF
    - Decision layer uses simple rule-based logic → near-instant output
    3) Memory
    - Only essential metadata features are loaded
    - Sparse data structures minimize memory usage
    4) Robustness
    - Very short text: rely more on metadata and previous_day_mood
    - Missing values: impute defaults or use median for numerical features
    - Contradictory input: uncertainty flag triggers safer recommendations


3. Edge Deployment Considerations

    1) Mobile Devices
    - Small memory footprint → runs on smartphones or tablets
    - TF-IDF + metadata computation lightweight
    2) Desktop / Laptop
    - Full-featured models for higher accuracy
    - Optional GUI / local API for interactive recommendations
    3) Tradeoffs
    - Smaller models → slightly lower accuracy but faster & lightweight
    - Longer TF-IDF vectors → higher accuracy but increased memory and latency
