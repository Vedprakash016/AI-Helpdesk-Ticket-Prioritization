import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data = pd.read_csv("tickets_dataset.csv")

print("Dataset loaded successfully!")
print("Total tickets:", len(data))


# -----------------------------
# CATEGORY MODEL
# -----------------------------

X = data["text"]
y_category = data["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_category,
    test_size=0.25,
    random_state=42,
    stratify=y_category
)

category_model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])

category_model.fit(X_train, y_train)

category_predictions = category_model.predict(X_test)

print("\nCATEGORY MODEL")
print("------------------------")
print(
    "Accuracy:",
    accuracy_score(y_test, category_predictions)
)
print(
    classification_report(
        y_test,
        category_predictions,
        zero_division=0
    )
)


# -----------------------------
# PRIORITY MODEL
# -----------------------------

y_priority = data["priority"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_priority,
    test_size=0.25,
    random_state=42,
    stratify=y_priority
)

priority_model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])

priority_model.fit(X_train, y_train)

priority_predictions = priority_model.predict(X_test)

print("\nPRIORITY MODEL")
print("------------------------")
print(
    "Accuracy:",
    accuracy_score(y_test, priority_predictions)
)
print(
    classification_report(
        y_test,
        priority_predictions,
        zero_division=0
    )
)


# -----------------------------
# SAVE MODELS
# -----------------------------

joblib.dump(
    category_model,
    "category_model.pkl"
)

joblib.dump(
    priority_model,
    "priority_model.pkl"
)

print("\nModels saved successfully!")