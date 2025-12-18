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
model = joblib.load(MODEL_PATH)

def predict(url:str):
    features = extract_features(url)
    prediction = model.predict([features])[0]
    confidence = model.predict_proba([features])[0][prediction]

    label = "phishing" if prediction == 1 else "legitimate"
    return label,round(confidence,4)
