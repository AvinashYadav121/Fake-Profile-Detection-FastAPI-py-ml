from tensorflow.keras.models import load_model

_model = None

def get_image_model():
    global _model
    if _model is None:
        _model = load_model("models/image_model.h5", compile=False)
    return _model
