# from image_ai.predict_image import get_image_score

# def analyze_profile_image(url):
#     return get_image_score(url)
# from image_ai.predict_image import get_image_score

# def analyze_image(url):
#     try:
#         score = get_image_score(url)
#         return score
#     except:
#         return 0.0

from image_ai.predict_image import get_image_score

def analyze_image(url):
    try:
        return get_image_score(url)
    except:
        return 0.0
