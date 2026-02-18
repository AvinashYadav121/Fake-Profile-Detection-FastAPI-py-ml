import numpy as np
import cv2
import requests
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions

model = MobileNetV2(weights="imagenet")

def is_animal(image_url):

    try:
        resp = requests.get(image_url, stream=True)
        img = np.asarray(bytearray(resp.content), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        img = cv2.resize(img, (224,224))
        img = preprocess_input(img)
        img = np.expand_dims(img, axis=0)

        preds = model.predict(img)
        labels = decode_predictions(preds)[0]

        animal_keywords = ["bird","dog","cat","horse","cow","sheep","elephant"]

        for _, label, prob in labels:
            if any(a in label.lower() for a in animal_keywords):
                return True

        return False

    except:
        return False
