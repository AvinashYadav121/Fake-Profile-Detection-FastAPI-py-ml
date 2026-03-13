
from services.human_detector import is_human_face
from services.cartoon_detector import is_cartoon
from services.object_detector import is_animal
from services.celebrity_check import is_celebrity
from image_ai.predict_image import get_image_score


def analyze_image(url):

    score = get_image_score(url)

    human = is_human_face(url)
    cartoon = is_cartoon(url)
    animal = is_animal(url)
    celeb = is_celebrity(url)

    risk = score

    if not human:
        risk += 0.3

    if cartoon:
        risk += 0.2

    if animal:
        risk += 0.3

    if celeb:
        risk += 0.4

    risk = min(risk, 1.0)

    # return TWO values
    return risk, human