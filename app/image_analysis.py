import cv2
import numpy as np


def analyze_affected_area(image):

    # PIL → NumPy
    if hasattr(image, "convert"):
        image = image.convert("RGB")
        image_rgb = np.array(image)
    else:
        image_rgb = np.array(image)

    # Resize
    image_rgb = cv2.resize(
        image_rgb,
        (224, 224)
    )

    # RGB → HSV
    hsv = cv2.cvtColor(
        image_rgb,
        cv2.COLOR_RGB2HSV
    )

    # ======================================
    # LEAF MASK
    # ======================================

    lower_green = np.array([20, 25, 20])
    upper_green = np.array([100, 255, 255])

    green_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    leaf_mask = cv2.morphologyEx(
        green_mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    leaf_mask = cv2.morphologyEx(
        leaf_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    # ======================================
    # YELLOW / BROWN REGIONS
    # ======================================

    lower_yellow = np.array([10, 40, 30])
    upper_yellow = np.array([40, 255, 255])

    yellow_mask = cv2.inRange(
        hsv,
        lower_yellow,
        upper_yellow
    )

    # ======================================
    # DARK REGIONS
    # ======================================

    lower_dark = np.array([0, 25, 0])
    upper_dark = np.array([180, 255, 95])

    dark_mask = cv2.inRange(
        hsv,
        lower_dark,
        upper_dark
    )

    # ======================================
    # COMBINE ABNORMAL REGIONS
    # ======================================

    abnormal_mask = cv2.bitwise_or(
        yellow_mask,
        dark_mask
    )

    abnormal_mask = cv2.bitwise_and(
        abnormal_mask,
        leaf_mask
    )

    small_kernel = np.ones(
        (3, 3),
        np.uint8
    )

    abnormal_mask = cv2.morphologyEx(
        abnormal_mask,
        cv2.MORPH_OPEN,
        small_kernel
    )

    # ======================================
    # AFFECTED PERCENTAGE
    # ======================================

    leaf_pixels = cv2.countNonZero(
        leaf_mask
    )

    affected_pixels = cv2.countNonZero(
        abnormal_mask
    )

    if leaf_pixels > 0:

        affected_percentage = (
            affected_pixels /
            leaf_pixels
        ) * 100

    else:

        affected_percentage = 0.0

    return {
        "image": image_rgb,
        "leaf_mask": leaf_mask,
        "affected_mask": abnormal_mask,
        "affected_percentage":
            float(affected_percentage)
    }