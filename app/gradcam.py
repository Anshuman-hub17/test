import cv2
import numpy as np
import tensorflow as tf


def find_mobilenet_model(model):
    """
    Find the nested MobileNetV2 model.
    """

    for layer in model.layers:

        if isinstance(layer, tf.keras.Model):

            if "mobilenet" in layer.name.lower():
                return layer

    raise ValueError(
        "MobileNetV2 model could not be found."
    )


def generate_gradcam(
    image,
    model,
    class_index=None
):
    """
    Generate Grad-CAM heatmap and overlay.
    """

    # ======================================
    # IMAGE PREPARATION
    # ======================================

    if hasattr(image, "convert"):
        image = image.convert("RGB")
        image_array = np.array(image)
    else:
        image_array = np.array(image)

    image_resized = cv2.resize(
        image_array,
        (224, 224)
    )

    image_tensor = tf.cast(
        image_resized,
        tf.float32
    )

    batch = tf.expand_dims(
        image_tensor,
        axis=0
    )

    # ======================================
    # FIND MOBILENET
    # ======================================

    mobilenet_model = find_mobilenet_model(
        model
    )

    last_conv_layer = mobilenet_model.get_layer(
        "out_relu"
    )

    conv_model = tf.keras.Model(
        inputs=mobilenet_model.input,
        outputs=last_conv_layer.output
    )

    # ======================================
    # PREPROCESS
    # ======================================

    preprocessed = (
        tf.keras.applications.mobilenet_v2
        .preprocess_input(batch)
    )

    # ======================================
    # GRAD-CAM
    # ======================================

    with tf.GradientTape() as tape:

        conv_outputs = conv_model(
            preprocessed,
            training=False
        )

        tape.watch(conv_outputs)

        x = conv_outputs

        start_processing = False

        for layer in mobilenet_model.layers:

            if layer.name == "out_relu":
                start_processing = True
                continue

            if start_processing:
                x = layer(
                    x,
                    training=False
                )

        mobile_index = model.layers.index(
            mobilenet_model
        )

        for layer in model.layers[
            mobile_index + 1:
        ]:

            x = layer(
                x,
                training=False
            )

        predictions = x

        if class_index is None:

            class_index = int(
                tf.argmax(
                    predictions[0]
                )
            )

        class_score = predictions[
            :,
            class_index
        ]

    # ======================================
    # GRADIENTS
    # ======================================

    gradients = tape.gradient(
        class_score,
        conv_outputs
    )

    pooled_gradients = tf.reduce_mean(
        gradients,
        axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(
        conv_outputs * pooled_gradients,
        axis=-1
    )

    heatmap = tf.maximum(
        heatmap,
        0
    )

    max_value = tf.reduce_max(
        heatmap
    )

    if max_value > 0:
        heatmap = heatmap / max_value

    heatmap = heatmap.numpy()

    # ======================================
    # CREATE OVERLAY
    # ======================================

    heatmap_resized = cv2.resize(
        heatmap,
        (224, 224)
    )

    heatmap_uint8 = np.uint8(
        255 * heatmap_resized
    )

    colored_heatmap = cv2.applyColorMap(
        heatmap_uint8,
        cv2.COLORMAP_JET
    )

    colored_heatmap = cv2.cvtColor(
        colored_heatmap,
        cv2.COLOR_BGR2RGB
    )

    overlay = cv2.addWeighted(
        image_resized,
        0.6,
        colored_heatmap,
        0.4,
        0
    )

    return {
        "heatmap": heatmap_resized,
        "colored_heatmap": colored_heatmap,
        "overlay": overlay
    }