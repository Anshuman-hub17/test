def format_prediction(class_name):

    plant, disease = class_name.split("___", 1)

    plant = (
        plant
        .replace("_", " ")
        .replace(",", "")
        .strip()
        .title()
    )

    disease = (
        disease
        .replace("_", " ")
        .strip()
        .title()
    )

    return plant, disease


def confidence_status(confidence):

    percentage = confidence * 100

    if percentage >= 85:
        return "High"

    elif percentage >= 65:
        return "Moderate"

    else:
        return "Low"


def prediction_message(confidence):

    percentage = confidence * 100

    if percentage >= 85:
        return "High confidence prediction."

    elif percentage >= 65:
        return (
            "Moderate confidence. "
            "Consider uploading another clear image."
        )

    else:
        return (
            "Low confidence. "
            "Prediction may be unreliable."
        )