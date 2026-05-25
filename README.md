# AI Emotion Tracker

A hybrid ML system that reads your journal entry and contextual metadata to predict your emotional state, measure its intensity, and tell you exactly what to do about it — and when.

---

## 📌 What This Project Does

Most mood trackers just log how you feel. This system goes further — it takes your journal text combined with contextual data (sleep hours, stress level, energy level, time of day, ambience) and runs it through a two-model ML pipeline to predict your emotional state and intensity, then a rule-based decision engine recommends a specific action with timing.

---

## ⚙️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Emotion Classification | Logistic Regression (Scikit-learn) |
| Intensity Prediction | XGBRegressor (XGBoost) |
| NLP | TF-IDF Vectorizer (5000 features, unigrams + bigrams) |
| Hyperparameter Tuning | GridSearchCV, RandomizedSearchCV |
| Web App | Flask |
| Frontend | HTML, CSS |
| Data | Pandas, NumPy, Matplotlib, Seaborn |

---

## 🧠 How the System Works

The pipeline has three stages:

**1. Feature Engineering**
- Journal text cleaned: lowercased, punctuation removed, stopwords filtered
- Text converted to TF-IDF vectors (5000 features, ngram_range 1–2)
- Metadata features (sleep, stress, energy, duration, text length, word count) scaled with StandardScaler
- Categorical features (ambience, time of day, previous mood, face emotion hint, reflection quality) one-hot encoded
- TF-IDF sparse matrix and metadata sparse matrix **stacked horizontally** using `scipy.sparse.hstack` into a single combined feature set

**2. Emotion Classification (Logistic Regression)**
- Predicts one of 6 emotional states from the combined feature set
- Tuned with GridSearchCV across C values [0.01, 0.1, 1, 10] and solvers [liblinear, lbfgs] with 5-fold cross validation
- Outputs class probabilities via `predict_proba` — confidence score extracted as max probability

**3. Intensity Prediction (XGBoost)**
- Predicts emotion intensity on a scale of 1–5 as a regression task
- XGBRegressor tuned with RandomizedSearchCV (n_estimators, max_depth, learning_rate, subsample, colsample_bytree)
- Output clipped and rounded to integer scale 1–5

**4. Uncertainty Modeling**
- If confidence score < 0.55 → `uncertain_flag = 1`
- If confidence score < 0.40 → decision engine returns default "pause / within_15_min" to avoid overconfident recommendations

**5. Rule-Based Decision Engine**
Takes predicted state + intensity + stress + energy + time of day and outputs:
- **What to do:** box breathing, deep work, grounding, journaling, rest, movement, light planning, pause
- **When to do it:** now, within 15 min, tonight, later today

| Condition | Action | Timing |
|---|---|---|
| High stress (≥4) or high intensity (≥4) | box_breathing | now |
| Low energy (≤2) at night/evening | rest | tonight |
| Low energy (≤2) other times | movement | within_15_min |
| High energy + focused state | deep_work | now |
| Anxious or restless | grounding | within_15_min |
| Sad or overwhelmed | journaling | tonight |
| Calm or content | light_planning | later_today |
| Confidence < 0.40 | pause | within_15_min |

---

## 🔬 Ablation Study Results

Ran a 3-way comparison to validate the combined input approach:

| Model | Input | Result |
|---|---|---|
| Text-only | TF-IDF features only | Lower accuracy |
| Metadata-only | Contextual features only | Lower accuracy |
| **Combined** | TF-IDF + metadata (hstack) | **Best accuracy** |

Combined approach outperformed both baselines — confirming that short or ambiguous journal entries benefit significantly from contextual metadata.

---

## 📁 File Structure

```
AI_emotion_tracker/
├── app.py                  # Flask web app
├── model.ipynb             # Full training notebook
├── models/
│   ├── emotion_model.pkl   # Saved Logistic Regression model
│   ├── intensity_model.pkl # Saved XGBRegressor model
│   ├── tfidf.pkl           # Saved TF-IDF vectorizer
│   └── scaler.pkl          # Saved StandardScaler
├── static/                 # CSS and frontend assets
├── templates/              # HTML templates
├── train_data.csv          # Training dataset
├── test_data.csv           # Test dataset
├── predictions.csv         # Model predictions output
├── EDGE_PLAN.md            # Edge case handling plan
└── ERROR_ANALYSIS.md       # Model error analysis
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/Kirtisharma2000/AI_emotion_tracker.git
cd AI_emotion_tracker

# 2. Install dependencies
pip install flask scikit-learn pandas numpy xgboost scipy

# 3. Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

