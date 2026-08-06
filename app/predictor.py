import pickle
from pathlib import Path

import numpy as np
import tensorflow as tf

from app.utils import (
    format_prediction,
    confidence_status,
    prediction_message
)


# ==========================================
# PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "plantvision_mobilenet_finetuned.keras"
)

CLASS_NAMES_PATH = (
    PROJECT_ROOT
    / "models"
    / "class_names.pkl"
)


# ==========================================
# LOAD MODEL
# ==========================================

print("Loading PlantVision model...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("Model loaded successfully!")


# ==========================================
# LOAD CLASS NAMES
# ==========================================

with open(CLASS_NAMES_PATH, "rb") as f:
    class_names = pickle.load(f)

print(
    f"Loaded {len(class_names)} disease classes."
)


# ==========================================
# IMAGE SETTINGS
# ==========================================

IMG_SIZE = (224, 224)


# ==========================================
# PREDICTION FUNCTION
# ==========================================

def predict_leaf(image):

    """
    Predict plant disease from an image.

    image:
        PIL Image, NumPy array,
        or TensorFlow-compatible image.
    """

    # PIL image → NumPy
    if hasattr(image, "convert"):
        image = image.convert("RGB")
        image = np.array(image)

    # Convert to Tensor
    image = tf.convert_to_tensor(image)

    # Make sure image has 3 channels
    if image.shape[-1] == 4:
        image = image[:, :, :3]

    # Resize
    image = tf.image.resize(
        image,
        IMG_SIZE
    )

    image = tf.cast(
        image,
        tf.float32
    )

    # Add batch dimension
    batch = tf.expand_dims(
        image,
        axis=0
    )

    # ======================================
    # MODEL PREDICTION
    # ======================================

    probabilities = model.predict(
        batch,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(probabilities)
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = float(
        probabilities[predicted_index]
    )

    plant, disease = format_prediction(
        predicted_class
    )

    # ======================================
    # TOP 3
    # ======================================

    top_indices = np.argsort(
        probabilities
    )[-3:][::-1]

    top_predictions = []

    for idx in top_indices:

        idx = int(idx)

        class_name = class_names[idx]

        top_plant, top_disease = (
            format_prediction(class_name)
        )

        top_predictions.append({
            "plant": top_plant,
            "disease": top_disease,
            "class": class_name,
            "confidence":
                float(probabilities[idx])
        })

    # ======================================
    # FINAL RESULT
    # ======================================

    return {
        "plant": plant,
        "disease": disease,
        "class": predicted_class,
        "class_index": predicted_index,
        "confidence": confidence,

        "confidence_status":
            confidence_status(confidence),

        "message":
            prediction_message(confidence),

        "top_predictions":
            top_predictions
    }