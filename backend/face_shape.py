from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from io import BytesIO

# Load your trained model
model = load_model('face-shape-model/face_shape_model.h5')

# Class labels
class_names = ["square", "oblong", "heart", "round", "oval"]

def classify_face_shape(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert('RGB').resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    preds = model.predict(img_array)
    pred_index = int(np.argmax(preds, axis=1)[0])
    return class_names[pred_index]

def recommend_styles(face_shape):
    recommendations = {
        "square": ["Long Waves", "Side-Parted Styles"],
        "oblong": ["Full Bangs", "Curls"],
        "heart": ["Chin-Length Bobs", "Side Bangs"],
        "round": ["Layered Long Hair", "Volume on Top"],
        "oval": ["Almost Any Style"]
    }
    return recommendations.get(face_shape, [])
