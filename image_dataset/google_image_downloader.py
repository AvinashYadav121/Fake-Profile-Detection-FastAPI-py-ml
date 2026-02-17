import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import quote
from PIL import Image
from io import BytesIO

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def download_images(query, folder, limit=100):

    os.makedirs(f"image_dataset/{folder}", exist_ok=True)

    search_url = f"https://www.google.com/search?tbm=isch&q={quote(query)}"

    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    images = soup.find_all("img")

    count = 0

    for img in images:

        try:
            src = img.get("src")

            if not src or "http" not in src:
                continue

            img_data = requests.get(src).content
            image = Image.open(BytesIO(img_data)).convert("RGB")

            path = f"image_dataset/{folder}/{count}.jpg"
            image.save(path)

            count += 1
            print(folder, "saved:", count)

            if count >= limit:
                break

        except:
            pass

# ----------- CATEGORIES -----------

categories = {
    "real": ["portrait headshot person"],
    "ai": ["AI generated face"],
    "stock": ["professional portrait stock"],
    "logo": ["company logo"],
    "noface": ["nature landscape"],
    "celeb": ["popular youtuber face"]
}

for cat, queries in categories.items():
    for q in queries:
        download_images(q, cat)

print("Download Complete 🚀")
