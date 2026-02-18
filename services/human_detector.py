import cv2
import mediapipe as mp
import numpy as np
import requests

mp_face = mp.solutions.face_detection.FaceDetection(model_selection=1)

def is_human_face(image_url):

    try:
        resp = requests.get(image_url, stream=True)
        img = np.asarray(bytearray(resp.content), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        results = mp_face.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        return results.detections is not None

    except:
        return False
