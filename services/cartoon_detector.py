import cv2
import numpy as np
import requests

def is_cartoon(image_url):

    try:
        resp = requests.get(image_url, stream=True)
        img = np.asarray(bytearray(resp.content), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        edge_ratio = np.sum(edges) / (img.shape[0] * img.shape[1])

        return edge_ratio > 0.15

    except:
        return False
