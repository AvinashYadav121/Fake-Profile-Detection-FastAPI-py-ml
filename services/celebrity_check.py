from deepface import DeepFace

CELEB_DB = "celebs/"

def is_celebrity(image_path):

    try:
        result = DeepFace.find(img_path=image_path,
                               db_path=CELEB_DB,
                               enforce_detection=False)

        return len(result[0]) > 0

    except:
        return False
