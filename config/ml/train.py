import pandas as pd 
import os
import joblib
from feature_extraction import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split,StratifiedKFold,cross_val_score
from sklearn.metrics import accuracy_score,classification_report,f1_score

DATA_PATH = "phikita_dataset.csv"
ARTIFACTS = "artifacts"
MODEL_PATH = os.path.join(ARTIFACTS,"random_forest_model.pkl")

RANDOM_STATE = 42
TEST_SIZE = 0.2
N_SPLITS = 5


# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv(DATA_PATH)
df["status"] = df["status"].apply(lambda x: 1 if x == "phishing" else 0)


# -----------------------------
# FEATURE EXTRACTION
# -----------------------------

X = df["website"].apply(extract_features).tolist()
y = df["status"].values


# -----------------------------
# HOLD-OUT SPLIT
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)


# -----------------------------
# CROSS-VALIDATION
# -----------------------------

print("🔁 Running Stratified K-Fold Cross-Validation...")

rf_cv = RandomForestClassifier(
    n_estimators=200,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    class_weight="balanced"
)

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

cv_scores = cross_val_score(
    rf_cv,
    X_train,
    y_train,
    cv=skf,
    scoring="f1"
)

print(f"📊 CV F1 Scores: {cv_scores}")
print(f"📈 Mean CV F1 Score: {cv_scores.mean():.4f}")


# -----------------------------
# FINAL TRAINING
# -----------------------------

print("🚀 Training final model...")

final_model = RandomForestClassifier(
    n_estimators=200,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    class_weight="balanced"
)

final_model.fit(X_train, y_train)


# -----------------------------
# FINAL EVALUATION
# -----------------------------

y_pred = final_model.predict(X_test)

print("\n📄 Hold-out Test Set Evaluation:")
print(classification_report(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("Accuracy:",accuracy_score(y_test,y_pred))


# -----------------------------
# SAVE MODEL
# -----------------------------

os.makedirs(ARTIFACTS, exist_ok=True)
joblib.dump(final_model, MODEL_PATH)

print(f"\n💾 Model saved at: {MODEL_PATH}")