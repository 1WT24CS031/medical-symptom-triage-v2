from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.pipeline import Pipeline


# ==============================
# 1. Project paths
# ==============================

# train_model.py is inside the ml folder,
# so .parent.parent points to the main project folder.

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "symptoms.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "model.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"

MODEL_DIR.mkdir(exist_ok=True)


# ==============================
# 2. Load dataset
# ==============================

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

df = df.dropna()

df["symptoms"] = df["symptoms"].astype(str).str.lower().str.strip()
df["disease"] = df["disease"].astype(str).str.strip()

X = df["symptoms"]
y = df["disease"]

print(f"Total samples: {len(df)}")
print(f"Number of diseases: {y.nunique()}")


# ==============================
# 3. Train-test split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# ==============================
# 4. Build ML pipeline
# ==============================

pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=3000,
            random_state=42
        )
    )
])


# ==============================
# 5. Train model
# ==============================

print("\nTraining model...")

pipeline.fit(X_train, y_train)


# ==============================
# 6. Test model
# ==============================

y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"Accuracy: {accuracy * 100:.2f}%")


# ==============================
# 7. Classification report
# ==============================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ==============================
# 8. Cross-validation
# ==============================

print("\nRunning 4-fold cross-validation...")

cv = StratifiedKFold(
    n_splits=4,
    shuffle=True,
    random_state=42
)

cv_scores = cross_val_score(
    pipeline,
    X,
    y,
    cv=cv,
    scoring="accuracy"
)

print("\nCross-validation scores:")

for i, score in enumerate(cv_scores, start=1):
    print(f"Fold {i}: {score * 100:.2f}%")

print(f"\nMean CV Accuracy: {cv_scores.mean() * 100:.2f}%")
print(f"CV Standard Deviation: {cv_scores.std() * 100:.2f}%")


# ==============================
# 9. Confusion matrix
# ==============================

print("\nGenerating confusion matrix...")

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    xticks_rotation="vertical"
)

plt.title("Medical Symptom Classifier - Confusion Matrix")
plt.tight_layout()

CONFUSION_MATRIX_PATH = MODEL_DIR / "confusion_matrix.png"

plt.savefig(
    CONFUSION_MATRIX_PATH,
    dpi=300
)

plt.close()

print(f"Confusion matrix saved to: {CONFUSION_MATRIX_PATH}")


# ==============================
# 10. Save complete ML pipeline
# ==============================

print("\nSaving model...")

joblib.dump(
    pipeline,
    MODEL_PATH
)

print(f"Model saved to: {MODEL_PATH}")


# ==============================
# 11. Save TF-IDF vectorizer
# ==============================

vectorizer = pipeline.named_steps["tfidf"]

joblib.dump(
    vectorizer,
    VECTORIZER_PATH
)

print(f"Vectorizer saved to: {VECTORIZER_PATH}")


# ==============================
# 12. Finished
# ==============================

print("\n================================")
print("V2 MODEL TRAINING COMPLETED!")
print("================================")