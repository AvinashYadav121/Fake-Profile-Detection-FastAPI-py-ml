from deepface import DeepFace
import numpy as np
import pickle
import requests
from PIL import Image
from io import BytesIO

with open("celeb_embeddings.pkl", "rb") as f:
    celeb_db = pickle.load(f)

def cosine(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

def celebrity_match_score(url):

    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.save("temp.jpg")

        user_embed = DeepFace.represent(
            img_path="temp.jpg",
            model_name="Facenet"
        )[0]["embedding"]

        best = 0

        for celeb in celeb_db.values():
            sim = cosine(user_embed, celeb)
            best = max(best, sim)

        if best > 0.75:
            return 0.9   # celebrity detected
        elif best > 0.6:
            return 0.6   # possible
        else:
            return 0.1   # not celeb

    except:
        return 0.2
