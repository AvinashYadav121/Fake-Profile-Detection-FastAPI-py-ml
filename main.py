# import joblib
# import numpy as np
# import tensorflow as tf

# tabular_model = joblib.load("models/tabular_model.pkl")
# image_model = tf.keras.models.load_model("models/image_model.h5")

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
# # CORS CONFIG
# # =========================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
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
# # REQUEST SCHEMAS
# # =========================

# class PredictRequest(BaseModel):
#     dataset: str
#     algorithm: str | None = None
#     features: list

# class TrustRequest(BaseModel):
#     dataset: str
#     features: list

# # =========================
# # SINGLE PREDICTION
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
# # TRUST CHECK (NEW UPGRADE)
# # =========================

# @app.post("/trust-check")
# def trust_check(req: TrustRequest):

#     dataset = req.dataset
#     X = np.array(req.features).reshape(1, -1)

#     # Use best model automatically
#     model = models[dataset]["XGBoost"]

#     pred = model.predict(X)[0]

#     fake_score = 1 if pred == 1 else 0
#     trust_score = 1 - fake_score

#     if fake_score < 0.3:
#         risk = "Safe"
#     elif fake_score < 0.6:
#         risk = "Suspicious"
#     else:
#         risk = "High Risk"

#     return {
#         "fake_risk": fake_score,
#         "trust_score": trust_score,
#         "risk_level": risk,
#         "model_used": "XGBoost"
#     }

# # =========================
# # HEALTH CHECK
# # =========================

# @app.get("/")
# def health():
#     return {"status": "API is running 🚀"}



# from services.instagram_service import fetch_profile
# from services.feature_engineering import extract_features
# from services.image_service import analyze_image

# @app.get("/ai-detect/{username}")
# def ai_detect(username: str):

#     profile = fetch_profile(username)

#     if not profile:
#         return {"error": "Profile not found"}

#     # Tabular
#     features = extract_features(profile)
#     tab_score = float(tabular_model.predict_proba([features])[0][1])

#     # Image
#     image_model = None

# def get_image_model():
#     global image_model
#     if image_model is None:
#         image_model = tf.keras.models.load_model("models/image_model.h5")
#     return image_model

#     # Combine
#     final_score = (tab_score * 0.7) + (img_score * 0.3)

#     result = "Fake" if final_score > 0.5 else "Real"

#     return {
#         "username": profile["username"],
#         "followers": profile["followers"],
#         "posts": profile["posts"],
#         "tabular_score": round(tab_score,2),
#         "image_score": round(img_score,2),
#         "final_score": round(final_score,2),
#         "result": result
#     }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import tensorflow as tf
import numpy as np

from services.instagram_service import fetch_profile
from services.feature_engineering import extract_features
from services.image_service import analyze_image

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD TABULAR MODEL ----------------
tabular_model = joblib.load("models/tabular_model.pkl")

# ---------------- LAZY LOAD IMAGE MODEL ----------------
image_model = None

def get_image_model():
    global image_model
    if image_model is None:
        image_model = tf.keras.models.load_model("models/image_model.h5")
    return image_model

# ---------------- OLD ROUTES ----------------
@app.get("/")
def home():
    return {"status": "Backend running"}

# ---------------- NEW AI ROUTE ----------------
@app.get("/ai-detect/{username}")
def ai_detect(username: str):

    profile = fetch_profile(username)

    if not profile:
        return {"error": "Profile not found"}

    # Tabular score
    features = extract_features(profile)
    tab_score = float(tabular_model.predict_proba([features])[0][1])

    # Image score
    img_score = float(analyze_image(profile["profile_pic_url"]))

    # Final score
    final_score = (tab_score * 0.7) + (img_score * 0.3)

    result = "Fake" if final_score > 0.5 else "Real"

    return {
        "username": profile["username"],
        "followers": profile["followers"],
        "posts": profile["posts"],
        "tabular_score": round(tab_score, 3),
        "image_score": round(img_score, 3),
        "final_score": round(final_score, 3),
        "result": result
    }
