
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import joblib
# import numpy as np

# from services.instagram_service import fetch_profile
# from services.feature_engineering import extract_features
# from services.image_service import analyze_image
# from urllib.parse import quote, unquote
# from fastapi.responses import StreamingResponse
# import requests

# # =========================
# # APP INIT
# # =========================

# app = FastAPI()

# # =========================
# # CORS
# # =========================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # =========================
# # LOAD OLD MODELS
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

# # =========================
# # LOAD NEW TABULAR MODEL
# # =========================

# tabular_model = joblib.load("models/tabular_model.pkl")

# # =========================
# # REQUEST SCHEMAS
# # =========================

# class PredictRequest(BaseModel):
#     dataset: str
#     algorithm: str
#     features: list

# class TrustRequest(BaseModel):
#     dataset: str
#     features: list
# # =========================
# # Image
# # =========================
# @app.get("/image-proxy")
# def image_proxy(url: str):
#     decoded_url = unquote(unquote(url))
#     response = requests.get(decoded_url, stream=True)
#     return StreamingResponse(response.raw, media_type="image/jpeg")

# # =========================
# # HEALTH CHECK
# # =========================

# @app.get("/")
# def home():
#     return {"status": "Backend running 🚀"}

# # =========================
# # OLD ROUTE: SINGLE PREDICTION
# # =========================

# @app.post("/predict")
# def predict(req: PredictRequest):

#     model = models[req.dataset][req.algorithm]
#     X = np.array(req.features).reshape(1, -1)
#     pred = model.predict(X)[0]

#     return {
#         "prediction": "Fake Account" if pred == 1 else "Real Account",
#         "algorithm": req.algorithm
#     }

# # =========================
# # OLD ROUTE: COMPARE ALL
# # =========================

# @app.post("/predict-compare")
# def predict_compare(req: PredictRequest):

#     dataset = req.dataset
#     X = np.array(req.features).reshape(1, -1)

#     comparison = {}

#     for algo_name, model in models[dataset].items():
#         pred = model.predict(X)[0]

#         comparison[algo_name] = {
#             "prediction": "Fake Account" if pred == 1 else "Real Account"
#         }

#     return {
#         "dataset": dataset,
#         "comparison": comparison
#     }

# # =========================
# # OLD ROUTE: TRUST CHECK
# # =========================

# @app.post("/trust-check")
# def trust_check(req: TrustRequest):

#     model = models[req.dataset]["XGBoost"]
#     X = np.array(req.features).reshape(1, -1)

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
#         "risk_level": risk
#     }

# # =========================
# # NEW ROUTE: AI USERNAME DETECTION
# # =========================

# @app.get("/ai-detect/{username}")
# def ai_detect(username: str):

#     profile = fetch_profile(username)

#     if not profile:
#         return {"error": "Profile not found"}

#     # Tabular Score
#     features = extract_features(profile)
#     tab_score = float(tabular_model.predict_proba([features])[0][1])

#     # Image Score
#     img_score = float(analyze_image(profile["profile_pic_url"]))

#     # Final Fusion Score
#     final_score = (tab_score * 0.7) + (img_score * 0.3)

#     result = "Fake" if final_score > 0.5 else "Real"

#     return {
#         "username": profile["username"],
#         "followers": profile["followers"],
#         "posts": profile["posts"],
#         "profile_pic": f"http://localhost:8000/image-proxy?url={quote(quote(profile['profile_pic_url']))}",

#         "tabular_score": round(tab_score, 3),
#         "image_score": round(img_score, 3),
#         "final_score": round(final_score, 3),
#         "result": result
#     }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

from services.instagram_service import fetch_profile
from services.image_service import analyze_image

import networkx as nx

from urllib.parse import quote, unquote
from fastapi.responses import StreamingResponse
import requests

# =========================
# APP INIT
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD OLD MODELS
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

# =========================
# LOAD NEW TABULAR MODEL
# =========================

tabular_model = joblib.load("models/fake_profile_model.pkl")

# =========================
# REQUEST SCHEMAS
# =========================

class PredictRequest(BaseModel):
    dataset: str
    algorithm: str
    features: list

class TrustRequest(BaseModel):
    dataset: str
    features: list

# =========================
# IMAGE PROXY
# =========================

@app.get("/image-proxy")
def image_proxy(url: str):
    decoded_url = unquote(unquote(url))
    response = requests.get(decoded_url, stream=True)
    return StreamingResponse(response.raw, media_type="image/jpeg")

# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def home():
    return {"status": "Backend running 🚀"}

# =========================
# OLD ROUTE: SINGLE PREDICTION
# =========================

@app.post("/predict")
def predict(req: PredictRequest):

    model = models[req.dataset][req.algorithm]
    X = np.array(req.features).reshape(1, -1)
    pred = model.predict(X)[0]

    return {
        "prediction": "Fake Account" if pred == 1 else "Real Account",
        "algorithm": req.algorithm
    }

# =========================
# OLD ROUTE: COMPARE ALL
# =========================

@app.post("/predict-compare")
def predict_compare(req: PredictRequest):

    dataset = req.dataset
    X = np.array(req.features).reshape(1, -1)

    comparison = {}

    for algo_name, model in models[dataset].items():
        pred = model.predict(X)[0]

        comparison[algo_name] = {
            "prediction": "Fake Account" if pred == 1 else "Real Account"
        }

    return {
        "dataset": dataset,
        "comparison": comparison
    }

# =========================
# OLD ROUTE: TRUST CHECK
# =========================

@app.post("/trust-check")
def trust_check(req: TrustRequest):

    model = models[req.dataset]["XGBoost"]
    X = np.array(req.features).reshape(1, -1)

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
        "risk_level": risk
    }

# =========================
# FEATURE ENGINEERING (NEW)
# =========================

def build_features(profile):

    followers = profile["followers"]
    followings = profile["following"]
    posts = profile["posts"]

    bio = profile.get("bio", "")
    bio_len = len(bio)

    username = profile["username"]

    has_pic = 1 if profile["profile_pic_url"] else 0
    username_len = len(username)
    username_digits = sum(c.isdigit() for c in username)

    full_name_len = len(profile.get("full_name",""))

    is_private = profile.get("is_private",0)
    is_business = profile.get("is_business",0)
    is_recent_user = profile.get("is_recent_user",0)

    # =====================
    # Behavioral Features
    # =====================

    follow_ratio = followers / (followings + 1)

    follow_diff = followers - followings

    post_follower_ratio = posts / (followers + 1)

    activity_score = posts / (followings + 1)

    # =====================
    # Graph Features
    # =====================

    G = nx.Graph()

    user = "target"

    follower_node = f"followers_{followers}"
    following_node = f"following_{followings}"

    G.add_edge(user, follower_node)
    G.add_edge(user, following_node)

    degree = nx.degree_centrality(G)[user]

    clustering = nx.clustering(G, user)

    pagerank = nx.pagerank(G)[user]

    return [

        has_pic,
        username_len,
        username_digits,
        is_private,
        full_name_len,

        posts,
        followers,
        followings,
        bio_len,
        is_business,
        is_recent_user,

        follow_ratio,
        follow_diff,
        post_follower_ratio,
        activity_score,

        degree,
        clustering,
        pagerank
    ]

# =========================
# NEW ROUTE: AI USERNAME DETECTION
# =========================

@app.get("/ai-detect/{username}")
def ai_detect(username: str):

    profile = fetch_profile(username)

    if not profile:
        return {"error": "Profile not found"}

    # TABULAR MODEL
    features = build_features(profile)

    tab_score = float(
        tabular_model.predict_proba([features])[0][1]
    )

    # IMAGE MODEL
    img_score = float(
        analyze_image(profile["profile_pic_url"])
    )

    # FUSION
    final_score = (tab_score * 0.7) + (img_score * 0.3)

    result = "Fake" if final_score > 0.5 else "Real"

    return {

        "username": profile["username"],
        "followers": profile["followers"],
        "posts": profile["posts"],

        "profile_pic": f"http://localhost:8000/image-proxy?url={quote(quote(profile['profile_pic_url']))}",

        "tabular_score": round(tab_score,3),
        "image_score": round(img_score,3),
        "final_score": round(final_score,3),

        "result": result
    }