import requests

def save_profile_image(url, username):

    response = requests.get(url)

    path = f"images/profiles/{username}.jpg"

    with open(path, "wb") as f:
        f.write(response.content)

    return path