import os
import joblib
from django.conf import settings
from ml.feature_extraction import extract_features

# IMPORTANT:
# settings.BASE_DIR -> /opt/render/project/src/config
# We need repo root -> /opt/render/project/src
BASE_DIR = settings.BASE_DIR.parent

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "artifacts",
    "random_forest_model.pkl"
)

_model = None  # cached model instance


def get_model():
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"ML model not found at: {MODEL_PATH}"
            )

        _model = joblib.load(MODEL_PATH)

    return _model


def predict(url: str):
    model = get_model()

    # Extract features
    features = extract_features(url)

    # Ensure correct shape
    prediction = model.predict([features])[0]
    proba = model.predict_proba([features])[0]

    confidence = proba[int(prediction)]
    label = "phishing" if prediction == 1 else "legitimate"

    return label, round(float(confidence), 4)
