1. Overview

    This document analyzes 10 failure cases from the model’s predictions of emotional state and intensity.
    The goal is to understand why the model failed, the types of errors, and how to improve it.

    Focus areas:
    - Ambiguous or short text
    - Conflicting signals between text and metadata
    - Contradictory reflections
    - Noisy or inconsistent labels


2. Failure cases
 
| ID  | Journal Text / Hint                                 Actual State | Predicted State | Problem Type        | Why Failed                                                                   | Suggested Fix                                                   |

| 855 | face_emotion_hint=neutral                           |  calm         | mixed           | Conflicting signals | Text or hint neutral but actual calm → model overpredicted uncertainty       | Combine text + metadata weighting                               |
| 523 | “at first still anxious a bit.”                     |  calm         | overwhelmed     | Ambiguous text      | Text contains “anxious” but intensity is mild → model overpredicted          | Use metadata (stress, energy) to adjust prediction              |
| 765 | “Honestly helped me plan my day. Later it changed …” | mixed        | focused         | Contradictory text  | Text starts positive, ends conflicting → model underpredicted                | Use sentiment averaging or prioritize last sentence             |
| 676 | “i guess back to normal after.”                      | neutral      | mixed           | Short / vague       | Text too short to infer emotion                                              | Rely on metadata or previous_day_mood                           |
| 677 | “okay session …”                                     | calm         | overwhelmed     | Very short text     | One-word text doesn’t convey emotion → model overpredicts stress             | Fallback rules: if text <3 words, rely on metadata              |
| 598 | “For some reason still anxious a bit.”               | overwhelmed  | restless        | Conflicting signals | Text shows mild anxiety, metadata shows low stress → intensity overpredicted | Use uncertainty flag to avoid overconfident prediction          |
| 893 | “not gonna lie i felt okay overall…”                 | overwhelmed  | neutral         | Mixed signals       | Text positive, metadata indicates low energy → state mispredicted            | Weighted combination of text + metadata                         |
| 727 | “could focus for a while”                            | neutral      | overwhelmed     | Mixed / ambiguous   | Positive text but stress high → model misclassifies                          | Include stress + energy weighting in decision layer             |
| 596 | “mind was all over the place”                        | mixed        | focused         | Ambiguous text      | Text signals distraction, model predicted focused → intensity overpredicted  | Metadata should adjust prediction                               |
| 652 | “Honestly honestly not much change.”                 | neutral      | overwhelmed     | Vague / ambiguous   | Text indicates no change, model predicts high intensity                      | Rule: vague text + low intensity → use metadata & previous mood |


3. Key Insights

    1) Ambiguous or Short Text
     - Short entries or vague phrases (e.g., “okay session …”) lead to misclassification.
     - Fix: rely more on metadata and previous_day_mood.

    2) Conflicting Signals
     - Text may suggest one emotion while metadata suggests another (e.g., “still anxious a bit” + low stress).
     - Fix: weighted scoring between text and metadata; uncertainty flags.

    3) Contradictory or Mixed Sentiment
     - Some reflections contain multiple emotions.
     - Fix: consider sentence-level sentiment averaging or last-sentence prioritization.

    4) Model Overconfidence
     - Intensity is often under- or over-predicted.
     - Fix: implement confidence scoring; adjust intensity based on metadata.

    5) Short / Missing Context
     - Minimal text or missing metadata can mislead predictions.
     - Fix: fallback rules using previous mood, stress, energy levels, or time-of-day.


4. Conclusion

   - The system handles messy real-world input reasonably well but fails in ambiguous, short, or conflicting  cases.
   - Combining text + metadata, uncertainty awareness, and fallback rules significantly improves robustness.
   - Future improvements include multi-sentence sentiment analysis, label smoothing, and better handling of short reflections.


  
