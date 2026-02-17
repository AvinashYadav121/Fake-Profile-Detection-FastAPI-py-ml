from deepface import DeepFace
import os
import pickle

celeb_folder = "celebs"
embeddings = {}

for img in os.listdir(celeb_folder):
    path = os.path.join(celeb_folder, img)

    try:
        rep = DeepFace.represent(img_path=path, model_name="Facenet")[0]["embedding"]
        embeddings[img] = rep
        print("Encoded:", img)
    except:
        print("Skipped:", img)

with open("celeb_embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)

print("Saved celeb embeddings")
