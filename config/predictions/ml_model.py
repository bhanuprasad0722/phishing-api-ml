import os
import joblib
from django.conf import settings
from ml.feature_extraction import extract_features

# Repo root (/opt/render/project/src)
BASE_DIR = settings.BASE_DIR.parent

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "artifacts",
    "random_forest_model.pkl"
)

_model = None


def get_model():
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"ML model not found at: {MODEL_PATH}")

        _model = joblib.load(MODEL_PATH)

    return _model


def predict(url: str):
    model = get_model()

    features = extract_features(url)

    # 🚨 SAFETY CHECK
    if len(features) != 14:
        raise ValueError(f"Invalid feature length: {len(features)}")

    prediction = model.predict([features])[0]
    proba = model.predict_proba([features])[0]

    label = "phishing" if int(prediction) == 1 else "legitimate"
    confidence = float(proba[int(prediction)])

    return label, round(confidence, 4)
