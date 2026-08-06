from pathlib import Path
from PIL import Image

from app.predictor import predict_leaf


# Pick one Apple Scab image
folder = Path(
    "data/raw/PlantVillage/color/Apple___Apple_scab"
)

image_path = next(folder.glob("*"))

print("\nTesting image:")
print(image_path)

# Load image
image = Image.open(image_path)

# Predict
result = predict_leaf(image)


print("\nPLANTVISION AI RESULT")
print("=" * 45)

print("Plant:", result["plant"])
print("Disease:", result["disease"])

print(
    "Confidence:",
    f'{result["confidence"] * 100:.2f}%'
)

print(
    "Confidence Status:",
    result["confidence_status"]
)

print(
    "Message:",
    result["message"]
)


print("\nTOP 3 PREDICTIONS")
print("=" * 45)

for i, pred in enumerate(
    result["top_predictions"],
    start=1
):
    print(
        f"{i}. {pred['plant']} - "
        f"{pred['disease']} "
        f"({pred['confidence'] * 100:.2f}%)"
    )