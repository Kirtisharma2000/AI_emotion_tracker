# AI Emotion Tracker

A hybrid ML + rule-based system that reads your journal entry and metadata (sleep, stress, energy levels) to predict your emotional state and recommend what action to take — and when.

---

## 📌 What This Project Does

Most mood trackers just log how you feel. This system goes further — it predicts your emotional state from text + context, estimates how intense that emotion is, and then decides what you should do about it (breathing exercise, deep work, journaling, rest) and when (now, within 15 minutes, later today).

---

## ⚙️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| ML Models | Scikit-learn (Logistic Regression, Random Forest) |
| NLP | TF-IDF Vectorizer |
| Web App | Flask |
| Frontend | HTML, CSS |

---

## 🧠 How the System Works

The pipeline has three stages:

**1. Emotion Prediction (ML)**
- Input: journal text + metadata (sleep hours, stress level, energy level, time of day, previous mood, ambience)
- Text is converted to TF-IDF vectors; metadata is processed as numerical/categorical features
- Both are combined into a single feature set
- A **Logistic Regression** model predicts the emotional state

**2. Intensity Prediction (ML)**
- A **Random Forest Classifier** predicts emotion intensity on a scale of 1–5
- Treats intensity as an ordinal classification problem

**3. Decision Engine (Rule-Based)**
- Takes predicted state + intensity + metadata as input
- Outputs: what action to take + when to take it
- Examples: "Do a breathing exercise now", "Schedule deep work for later today"

---

## 🔬 Key Design Decisions

**Why combine text + metadata?**
Short or ambiguous journal entries ("feeling off") are hard to classify on text alone. Metadata (e.g., 4 hours of sleep, high stress) corrects for this. Ablation study confirmed: text + metadata model is more robust than text-only.

**Uncertainty Modeling**
- Every prediction includes a confidence score (0–1)
- If confidence < 0.6, an `uncertain_flag` is raised so the system doesn't make overconfident recommendations

---

## 📁 File Structure

```
AI_emotion_tracker/
├── app.py              # Flask web app
├── model.ipynb         # Full training notebook
├── models/             # Saved trained models
├── static/             # CSS and frontend assets
├── templates/          # HTML templates
├── train_data.csv      # Training dataset
├── test_data.csv       # Test dataset
├── predictions.csv     # Sample model predictions
├── EDGE_PLAN.md        # Edge case handling plan
└── ERROR_ANALYSIS.md   # Model error analysis
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/Kirtisharma2000/AI_emotion_tracker.git
cd AI_emotion_tracker

# 2. Install dependencies
pip install flask scikit-learn pandas numpy

# 3. Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.
