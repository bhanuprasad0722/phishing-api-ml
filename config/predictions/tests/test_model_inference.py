import joblib
from ml.feature_extraction import extract_features
import pytest
import os

MODEL_PATH = "config/ml/artifacts/random_forest_model.pkl"

@pytest.mark.skipif(os.getenv("GITHUB_ACTIONS") == "true", reason="Skip ML model test in CI")
def test_model_loads():
    model = joblib.load(MODEL_PATH)
    assert model is not None

@pytest.mark.skipif(os.getenv("GITHUB_ACTIONS") == "true", reason="Skip ML model test in CI")
def test_model_prediction_output():
    model = joblib.load(MODEL_PATH)

    url = "https://google.com"
    features = extract_features(url)

    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]

    assert prediction in [0, 1]
    assert len(probabilities) == 2
    assert 0.0 <= probabilities[0] <= 1.0
    assert 0.0 <= probabilities[1] <= 1.0
