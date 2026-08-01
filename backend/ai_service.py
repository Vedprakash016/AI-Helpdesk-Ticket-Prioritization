from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent
AI_MODEL_DIR = BASE_DIR.parent / "ai-model"

CATEGORY_MODEL_PATH = AI_MODEL_DIR / "category_model.pkl"
PRIORITY_MODEL_PATH = AI_MODEL_DIR / "priority_model.pkl"


category_model = joblib.load(CATEGORY_MODEL_PATH)
priority_model = joblib.load(PRIORITY_MODEL_PATH)


def predict_ticket(title: str, description: str):
    ticket_text = f"{title} {description}"

    category = category_model.predict([ticket_text])[0]
    priority = priority_model.predict([ticket_text])[0]

    category_confidence = float(
        category_model.predict_proba([ticket_text]).max()
    )

    priority_confidence = float(
        priority_model.predict_proba([ticket_text]).max()
    )

    priority_score = round(priority_confidence * 100)

    return {
        "category": category,
        "priority": priority,
        "priority_score": priority_score,
        "category_confidence": round(category_confidence * 100, 2),
        "priority_confidence": round(priority_confidence * 100, 2)
    }