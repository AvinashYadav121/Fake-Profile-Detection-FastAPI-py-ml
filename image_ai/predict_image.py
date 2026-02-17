# import tensorflow as tf
# import numpy as np
# from PIL import Image
# import requests
# from io import BytesIO

# model = tf.keras.models.load_model("image_ai/image_model.h5")

# class_map = {
#     0: "ai",
#     1: "celeb",
#     2: "logo",
#     3: "noface",
#     4: "real",
#     5: "stock"
# }

# fake_score_map = {
#     "real": 0.1,
#     "stock": 0.5,
#     "logo": 0.6,
#     "noface": 0.7,
#     "celeb": 0.8,
#     "ai": 0.9
# }

# def get_image_score(url):

#     try:
#         response = requests.get(url)
#         img = Image.open(BytesIO(response.content)).resize((128,128))
#         img = np.array(img)/255.0
#         img = np.expand_dims(img, axis=0)

#         pred = model.predict(img)
#         label = class_map[np.argmax(pred)]

#         return fake_score_map[label]

#     except:
#         return 0.6

import requests
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from main import get_image_model

def get_image_score(url):

    try:
        response = requests.get(url, timeout=5)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        img = img.resize((224,224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        model = get_image_model()
        prediction = model.predict(img)[0][0]

        return float(prediction)

    except:
        return 0.0
