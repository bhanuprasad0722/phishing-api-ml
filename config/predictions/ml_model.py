import joblib
from ml.feature_extraction import extract_features
import os
from django.conf import settings

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
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
                f"ML model not found at {MODEL_PATH}. "
                "Make sure the model is available in production."
            )
        _model = joblib.load(MODEL_PATH)

    return _model


def predict(url: str):
    model = get_model()

    features = extract_features(url)
    prediction = model.predict([features])[0]
    confidence = model.predict_proba([features])[0][prediction]

    label = "phishing" if prediction == 1 else "legitimate"
    return label, round(confidence, 4)
