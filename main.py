
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import networkx as nx

from services.instagram_service import fetch_profile
from services.image_service import analyze_image

from urllib.parse import quote, unquote
from fastapi.responses import StreamingResponse
import requests
from database import conn
# from admin_routes import router as admin_router



# =========================
# APP INIT
# =========================

app = FastAPI()

# app.include_router(admin_router)
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
# OLD ROUTE: COMPARE MODELS
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
# TRUST CHECK
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
# FEATURE ENGINEERING
# =========================

def build_features(profile):

    followers = profile["followers"]
    followings = profile["following"]
    posts = profile["posts"]

    bio = profile.get("bio", "")

    username = profile["username"]

    has_pic = 1 if profile.get("profile_pic_url") else 0

    username_len = len(username)

    username_digits = sum(c.isdigit() for c in username)

    full_name_len = len(profile.get("full_name", ""))

    is_private = profile.get("is_private", 0)

    is_business = profile.get("is_business", 0)

    is_recent_user = profile.get("is_recent_user", 0)

    bio_len = len(bio)

    follow_ratio = followers / (followings + 1)

    follow_diff = followers - followings

    post_follower_ratio = posts / (followers + 1)

    activity_score = posts / (followings + 1)

    # Graph Features
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
# AI USERNAME DETECTION
# =========================

@app.get("/ai-detect/{username}")
def ai_detect(username: str):

    profile = fetch_profile(username)

    if not profile:
        return {"error": "Profile not found"}

    # Tabular model
    features = build_features(profile)

    tab_score = float(
        tabular_model.predict_proba([features])[0][1]
    )

    # Image model
    img_score, face_detected = analyze_image(
        profile["profile_pic_url"]
    )

    # Fusion score
    final_score = (tab_score * 0.7) + (img_score * 0.3)

    result = "Fake" if final_score > 0.5 else "Real"

    bio = profile.get("bio", "")

    return {

        "username": profile["username"],

        "followers": profile["followers"],
        "following": profile["following"],
        "posts": profile["posts"],

        "followers_following_ratio":
            profile["followers"] / profile["following"]
            if profile["following"] else profile["followers"],

        "bio_length": len(bio),

        "bio_has_link": "http" in bio,

        "username_digit_count":
            sum(c.isdigit() for c in profile["username"]),

        "is_private": profile.get("is_private", 0),

        "highlight_count": profile.get("highlight_count", 0),

        "has_profile_pic":
            1 if profile.get("profile_pic_url") else 0,

        "profile_image_face_detected": face_detected,

        "profile_pic":
            f"http://localhost:8000/image-proxy?url={quote(quote(profile['profile_pic_url']))}",

        "tabular_score": round(tab_score, 3),

        "image_score": round(img_score, 3),

        "final_score": round(final_score, 3),

        "result": result
    }
    
from fastapi import Body
from database import conn

@app.post("/save-feedback")
def save_feedback(data: dict = Body(...)):

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO feedback_data(

            username,
            followers,
            following,
            posts,

            followers_following_ratio,

            bio_length,
            bio_has_link,
            username_digit_count,

            is_private,
            highlight_count,

            has_profile_pic,
            profile_image_face_detected,

            model_prediction,
            user_feedback,

            image_path

        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """,(

        data["username"],
        data["followers"],
        data["following"],
        data["posts"],

        data["followers_following_ratio"],

        data["bio_length"],
        bool(data["bio_has_link"]),
        data["username_digit_count"],

        bool(data["is_private"]),
        data["highlight_count"],

        bool(data["has_profile_pic"]),
        bool(data["profile_image_face_detected"]),

        data["model_prediction"],
        data["user_feedback"],

        data.get("image_path")   # profile image url

        ))

        conn.commit()

        return {"status":"saved"}

    except Exception as e:

        conn.rollback()

        print("Database error:", e)

        return {"error": str(e)}

    finally:

        cursor.close()
        


from fastapi import Request

@app.get("/admin/dashboard")
def admin_dashboard(request: Request):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            username,
            followers,
            following,
            posts,
            followers_following_ratio,
            model_prediction,
            user_feedback
        FROM feedback_data
        ORDER BY followers DESC
    """)

    rows = cursor.fetchall()

    data = []

    for r in rows:
        data.append({
            "username": r[0],
            "followers": r[1],
            "following": r[2],
            "posts": r[3],
            "ratio": r[4],
            "prediction": r[5],
            "feedback": r[6]
        })

    cursor.close()

    return data

