
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Allow frontend access
# 🔐 CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load models
models = {
    "dataset1": {
        "RandomForest": joblib.load("models/rf_dataset1.pkl"),
        "LightGBM": joblib.load("models/lgbm_dataset1.pkl"),
        "XGBoost": joblib.load("models/xgb_dataset1.pkl"),
    },
    "dataset2": {
        "RandomForest": joblib.load("models/rf_dataset2.pkl"),
        "LightGBM": joblib.load("models/lgbm_dataset2.pkl"),
        "XGBoost": joblib.load("models/xgb_dataset2.pkl"),
    }
}

accuracies = {
    "dataset1": {
        "RandomForest": 95.38,
        "LightGBM": 97.77,
        "XGBoost": 98.41
    },
    "dataset2": {
        "RandomForest": 94.12,
        "LightGBM": 96.85,
        "XGBoost": 97.63
    }
}

class PredictRequest(BaseModel):
    dataset: str
    algorithm: str
    features: list

@app.post("/predict")
def predict(req: PredictRequest):
    model = models[req.dataset][req.algorithm]
    X = np.array(req.features).reshape(1, -1)
    pred = model.predict(X)[0]

    return {
        "prediction": "Fake Account" if pred == 1 else "Real Account",
        "algorithm": req.algorithm,
        "accuracy": accuracies[req.dataset][req.algorithm],
        "comparison": accuracies[req.dataset]
    }



from instagram_fetch import fetch_instagram_profile
from instagram_fetch import map_to_dataset1, map_to_dataset2

@app.post("/predict-instagram")
def predict_instagram(username: str, dataset: str, algorithm: str):
    insta_data = fetch_instagram_profile(username)

    if dataset == "dataset1":
        features = map_to_dataset1(insta_data)
    else:
        features = map_to_dataset2(insta_data)

    model = models[dataset][algorithm]
    pred = model.predict([features])[0]

    return {
        "username": username,
        "prediction": "Fake Account" if pred == 1 else "Real Account",
        "algorithm": algorithm,
        "dataset": dataset,
        "used_features": features
    }

@app.post("/predict-compare")
def predict_compare(req: PredictRequest):
    dataset = req.dataset
    features = np.array(req.features).reshape(1, -1)

    results = {}

    for algo_name, model in models[dataset].items():
        pred = model.predict(features)[0]
        results[algo_name] = {
            "prediction": "Fake Account" if pred == 1 else "Real Account",
            "accuracy": accuracies[dataset][algo_name]
        }

    return {
        "dataset": dataset,
        "results": results
    }
