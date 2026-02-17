

# from pydantic import BaseModel

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import joblib
# import numpy as np

# # =========================
# # APP INIT
# # =========================

# app = FastAPI()

# # =========================
# # CORS CONFIG (MANDATORY)
# # =========================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # for production you can restrict later
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # =========================
# # LOAD MODELS
# # =========================

# models = {
#     "dataset1": {
#         "RandomForest": joblib.load("models/rf_dataset1.pkl"),
#         "LightGBM": joblib.load("models/lgbm_dataset1.pkl"),
#         "XGBoost": joblib.load("models/xgb_dataset1.pkl"),
#     },
#     "dataset2": {
#         "RandomForest": joblib.load("models/rf_dataset2.pkl"),
#         "LightGBM": joblib.load("models/lgbm_dataset2.pkl"),
#         "XGBoost": joblib.load("models/xgb_dataset2.pkl"),
#     }
# }

# accuracies = {
#     "dataset1": {
#         "RandomForest": 95.38,
#         "LightGBM": 97.77,
#         "XGBoost": 98.41,
#     },
#     "dataset2": {
#         "RandomForest": 94.12,
#         "LightGBM": 96.85,
#         "XGBoost": 97.63,
#     },
# }

# # =========================
# # REQUEST SCHEMA
# # =========================

# class PredictRequest(BaseModel):
#     dataset: str
#     algorithm: str | None = None
#     features: list

# # =========================
# # SINGLE ALGORITHM PREDICTION
# # =========================

# @app.post("/predict")
# def predict(req: PredictRequest):
#     model = models[req.dataset][req.algorithm]

#     X = np.array(req.features).reshape(1, -1)
#     pred = model.predict(X)[0]

#     return {
#         "prediction": "Fake Account" if pred == 1 else "Real Account",
#         "algorithm": req.algorithm,
#         "accuracy": accuracies[req.dataset][req.algorithm],
#     }

# # =========================
# # COMPARE ALL ALGORITHMS
# # =========================

# @app.post("/predict-compare")
# def predict_compare(req: PredictRequest):
#     dataset = req.dataset
#     X = np.array(req.features).reshape(1, -1)

#     comparison = {}

#     for algo_name, model in models[dataset].items():
#         pred = model.predict(X)[0]

#         comparison[algo_name] = {
#             "prediction": "Fake Account" if pred == 1 else "Real Account",
#             "accuracy": accuracies[dataset][algo_name],
#         }

#     return {
#         "dataset": dataset,
#         "comparison": comparison
#     }

# # =========================
# # HEALTH CHECK (OPTIONAL)
# # =========================

# @app.get("/")
# def health():
#     return {"status": "API is running 🚀"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

# =========================
# APP INIT
# =========================

app = FastAPI()

# =========================
# CORS CONFIG
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD MODELS
# =========================

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
        "XGBoost": 98.41,
    },
    "dataset2": {
        "RandomForest": 94.12,
        "LightGBM": 96.85,
        "XGBoost": 97.63,
    },
}

# =========================
# REQUEST SCHEMAS
# =========================

class PredictRequest(BaseModel):
    dataset: str
    algorithm: str | None = None
    features: list

class TrustRequest(BaseModel):
    dataset: str
    features: list

# =========================
# SINGLE PREDICTION
# =========================

@app.post("/predict")
def predict(req: PredictRequest):
    model = models[req.dataset][req.algorithm]

    X = np.array(req.features).reshape(1, -1)
    pred = model.predict(X)[0]

    return {
        "prediction": "Fake Account" if pred == 1 else "Real Account",
        "algorithm": req.algorithm,
        "accuracy": accuracies[req.dataset][req.algorithm],
    }

# =========================
# COMPARE ALL ALGORITHMS
# =========================

@app.post("/predict-compare")
def predict_compare(req: PredictRequest):
    dataset = req.dataset
    X = np.array(req.features).reshape(1, -1)

    comparison = {}

    for algo_name, model in models[dataset].items():
        pred = model.predict(X)[0]

        comparison[algo_name] = {
            "prediction": "Fake Account" if pred == 1 else "Real Account",
            "accuracy": accuracies[dataset][algo_name],
        }

    return {
        "dataset": dataset,
        "comparison": comparison
    }

# =========================
# TRUST CHECK (NEW UPGRADE)
# =========================

@app.post("/trust-check")
def trust_check(req: TrustRequest):

    dataset = req.dataset
    X = np.array(req.features).reshape(1, -1)

    # Use best model automatically
    model = models[dataset]["XGBoost"]

    pred = model.predict(X)[0]

    fake_score = 1 if pred == 1 else 0
    trust_score = 1 - fake_score

    if fake_score < 0.3:
        risk = "Safe"
    elif fake_score < 0.6:
        risk = "Suspicious"
    else:
        risk = "High Risk"

    return {
        "fake_risk": fake_score,
        "trust_score": trust_score,
        "risk_level": risk,
        "model_used": "XGBoost"
    }

# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def health():
    return {"status": "API is running 🚀"}

