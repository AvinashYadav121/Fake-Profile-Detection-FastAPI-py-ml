import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import quote
from PIL import Image
from io import BytesIO
from celebrity_list import global_celebrities, indian_celebrities

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SAVE_PATH = "image_dataset/celeb"
os.makedirs(SAVE_PATH, exist_ok=True)

MAX_TOTAL = 100
saved_count = 0


def download_celeb_images(name):

    global saved_count

    if saved_count >= MAX_TOTAL:
        return

    query = f"{name} portrait face"

    url = f"https://www.google.com/search?tbm=isch&q={quote(query)}"

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    images = soup.find_all("img")

    for img in images:

        if saved_count >= MAX_TOTAL:
            return

        try:
            src = img.get("src")

            if not src or "http" not in src:
                continue

            img_data = requests.get(src).content
            image = Image.open(BytesIO(img_data)).convert("RGB")

            filename = f"{SAVE_PATH}/{name}_{saved_count}.jpg"
            image.save(filename)

            saved_count += 1
            print("Saved:", filename)

        except:
            pass


# Download from global list
for celeb in global_celebrities:
    download_celeb_images(celeb)

# Download from Indian list
for celeb in indian_celebrities:
    download_celeb_images(celeb)

print("Done. Total images:", saved_count)
