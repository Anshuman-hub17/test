import streamlit as st
from PIL import Image

from predictor import (
    predict_leaf,
    model
)

from image_analysis import analyze_affected_area
from gradcam import generate_gradcam
from disease_info import get_disease_info
from report_generator import generate_pdf_report


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PlantVision AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Main hero */
    .hero {
        padding: 30px 35px;
        border-radius: 20px;
        background:
            linear-gradient(
                135deg,
                rgba(20, 83, 45, 0.35),
                rgba(6, 78, 59, 0.15)
            );
        border: 1px solid rgba(74, 222, 128, 0.18);
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 0px;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 12px;
        margin-bottom: 12px;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(74, 222, 128, 0.25);
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Section headings */
    .section-title {
        font-size: 1.6rem;
        font-weight: 750;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .section-description {
        opacity: 0.65;
        margin-bottom: 20px;
    }

    /* Diagnosis card */
    .diagnosis-card {
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(74, 222, 128, 0.18);
        background: rgba(22, 101, 52, 0.08);
        margin-bottom: 15px;
    }

    .diagnosis-label {
        font-size: 0.8rem;
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 3px;
    }

    .diagnosis-value {
        font-size: 1.7rem;
        font-weight: 700;
        margin-bottom: 18px;
    }

    /* Information card */
    .info-card {
        padding: 18px;
        border-radius: 14px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 12px;
    }

    /* Footer */
    .footer {
        text-align: center;
        opacity: 0.5;
        font-size: 0.8rem;
        padding-top: 30px;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        border-radius: 16px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        padding: 14px;
        border-radius: 14px;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
    }

    /* Images */
    [data-testid="stImage"] img {
        border-radius: 14px;
    }

    /* Progress */
    .stProgress > div > div > div > div {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🌿 PlantVision")

    st.caption(
        "AI-powered plant disease detection"
    )

    st.divider()

    st.subheader("🧠 AI Model")

    st.write(
        """
        **Architecture:** MobileNetV2

        **Input:** Leaf image

        **Image size:** 224 × 224

        **Classes:** 27

        **Explainability:** Grad-CAM
        """
    )

    st.divider()

    st.subheader("🌱 Supported Plants")

    st.write(
        """
        • Apple

        • Corn (Maize)

        • Grape

        • Bell Pepper

        • Potato

        • Tomato
        """
    )

    st.divider()

    st.subheader("🔬 Analysis")

    st.write(
        """
        PlantVision combines:

        **Deep Learning**  
        Disease classification

        **Computer Vision**  
        Visual abnormality estimation

        **Explainable AI**  
        Grad-CAM attention mapping
        """
    )

    st.divider()

    st.caption(
        "⚠️ PlantVision is an AI-based analysis "
        "tool and should not replace professional "
        "agricultural diagnosis."
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-badge">AI • Computer Vision • Explainable AI</div>
    <div class="hero-title">🌿 PlantVision AI</div>
    <div class="hero-subtitle">
        Intelligent plant disease detection and visual leaf analysis powered by deep learning.
    </div>
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<div class="section-title">Analyze a Leaf</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="section-description">
    Upload a clear image of a supported plant leaf
    to begin the AI analysis.
</div>
""",
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "Upload leaf image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ],
    label_visibility="collapsed"
)


# =========================================================
# EMPTY STATE
# =========================================================

if uploaded_file is None:

    st.info(
        "👆 Upload a leaf image to start the analysis."
    )

    st.markdown(
        """
<div class="info-card">

<b>📸 For better results</b><br><br>

• Use a clear, well-lit leaf image.<br>
• Keep the leaf visible and in focus.<br>
• Avoid excessive blur or very dark images.<br>
• Use one of the supported plant species.

</div>
""",
        unsafe_allow_html=True
    )


# =========================================================
# ANALYSIS
# =========================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")


    # =====================================================
    # RUN ALL ANALYSIS
    # =====================================================

    with st.spinner(
        "🌿 PlantVision is analyzing the leaf..."
    ):

        # Disease prediction
        result = predict_leaf(
            image
        )

        # Disease knowledge
        disease_details = get_disease_info(
            result["class"]
        )

        # OpenCV analysis
        area_result = analyze_affected_area(
            image
        )

        # Grad-CAM
        gradcam_result = generate_gradcam(
            image,
            model,
            result["class_index"]
        )


    # =====================================================
    # AI DIAGNOSIS
    # =====================================================

    st.markdown(
        '<div class="section-title">🧠 AI Diagnosis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="section-description">
    Primary prediction generated by the MobileNetV2
    disease classification model.
</div>
""",
        unsafe_allow_html=True
    )


    image_col, diagnosis_col = st.columns(
        [1.05, 1],
        gap="large"
    )


    # -----------------------------------------------------
    # UPLOADED IMAGE
    # -----------------------------------------------------

    with image_col:

        st.image(
            image,
            caption="Uploaded Leaf",
            width="stretch"
        )


    # -----------------------------------------------------
    # DIAGNOSIS
    # -----------------------------------------------------

    with diagnosis_col:

        st.subheader("AI Analysis")

        st.write("Plant")
        st.markdown(
            f"## {result['plant']}"
        )

        st.write("Disease")
        st.markdown(
            f"## {result['disease']}"
        )

        confidence_percentage = (
            result["confidence"] * 100
        )

        st.write("Confidence")
        st.markdown(
            f"## {confidence_percentage:.2f}%"
        )

        status = result[
            "confidence_status"
        ]

        if status == "High":

            st.success(
                result["message"]
            )

        elif status == "Moderate":

            st.warning(
                result["message"]
            )

        else:

            st.error(
                result["message"]
            )


    # =====================================================
    # TOP 3 PREDICTIONS
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Prediction Ranking</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="section-description">
    The three classes with the highest prediction probabilities.
</div>
""",
        unsafe_allow_html=True
    )


    top_columns = st.columns(3)


    for column, pred, rank in zip(
        top_columns,
        result["top_predictions"],
        range(1, 4)
    ):

        with column:

            probability = (
                pred["confidence"] * 100
            )

            st.markdown(
                f"### #{rank}"
            )

            st.write(
                f"**{pred['plant']}**"
            )

            st.write(
                pred["disease"]
            )

            st.progress(
                float(pred["confidence"])
            )

            st.caption(
                f"{probability:.2f}% confidence"
            )


    # =====================================================
    # VISUAL LEAF ANALYSIS
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">🔬 Visual Leaf Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="section-description">
    Computer-vision analysis used to estimate visually
    abnormal regions of the uploaded leaf.
</div>
""",
        unsafe_allow_html=True
    )


    analysis1, analysis2, analysis3 = st.columns(
        3
    )


    with analysis1:

        st.image(
            area_result["image"],
            caption="Original Leaf",
            width="stretch"
        )


    with analysis2:

        st.image(
            area_result["leaf_mask"],
            caption="Detected Leaf Region",
            width="stretch",
            clamp=True
        )


    with analysis3:

        st.image(
            area_result["affected_mask"],
            caption="Visually Abnormal Regions",
            width="stretch",
            clamp=True
        )


    affected = area_result[
        "affected_percentage"
    ]


    st.metric(
        "Estimated Visually Affected Area",
        f"{affected:.2f}%"
    )


    st.caption(
        "This percentage is estimated using image "
        "color and region analysis. It is not an "
        "exact biological disease-severity measurement."
    )


    # =====================================================
    # EXPLAINABLE AI — GRAD-CAM
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">🔥 Explainable AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="section-description">
    Grad-CAM helps visualize which image regions influenced
    the neural network's prediction.
</div>
""",
        unsafe_allow_html=True
    )


    grad1, grad2, grad3 = st.columns(
        3
    )


    with grad1:

        st.image(
            area_result["image"],
            caption="Original Leaf",
            width="stretch"
        )


    with grad2:

        st.image(
            gradcam_result[
                "colored_heatmap"
            ],
            caption="AI Attention Heatmap",
            width="stretch"
        )


    with grad3:

        st.image(
            gradcam_result[
                "overlay"
            ],
            caption="Grad-CAM Overlay",
            width="stretch"
        )


    st.info(
        "🔥 Warmer regions indicate stronger model "
        "attention. Grad-CAM shows where the model "
        "focused when producing its prediction; it "
        "does not independently identify diseased tissue."
    )


    # =====================================================
    # PLANT HEALTH GUIDANCE
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">🌱 Plant Health Guidance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="section-description">
    General educational information related to the
    condition identified by PlantVision.
</div>
""",
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # HEALTH / DISEASE STATUS
    # -----------------------------------------------------

    if disease_details["healthy"]:

        st.success(
            "🌿 The model classified this leaf as healthy."
        )

    else:

        st.warning(
            f'🦠 Predicted condition: {result["disease"]}'
        )


    # -----------------------------------------------------
    # ABOUT
    # -----------------------------------------------------

    st.markdown(
        "### 📖 About"
    )

    st.write(
        disease_details["about"]
    )


    # -----------------------------------------------------
    # COMMON VISUAL SIGNS
    # -----------------------------------------------------

    if disease_details["symptoms"]:

        st.markdown(
            "### 👁️ Common Visual Signs"
        )

        for symptom in disease_details[
            "symptoms"
        ]:

            st.write(
                f"• {symptom}"
            )


    # -----------------------------------------------------
    # NEXT STEPS + PREVENTION
    # -----------------------------------------------------

    action_col, prevention_col = st.columns(
        2,
        gap="large"
    )


    with action_col:

        st.markdown(
            "### 🛠️ Suggested Next Steps"
        )

        for action in disease_details[
            "actions"
        ]:

            st.write(
                f"• {action}"
            )


    with prevention_col:

        st.markdown(
            "### 🛡️ Prevention"
        )

        for prevention in disease_details[
            "prevention"
        ]:

            st.write(
                f"• {prevention}"
            )


    st.caption(
        "PlantVision provides general educational guidance. "
        "Disease management may vary depending on crop variety, "
        "location, climate, growing conditions, and severity. "
        "For serious or rapidly spreading problems, consult a "
        "qualified local agricultural professional."
    )


    # =====================================================
    # ANALYSIS SUMMARY
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📋 Analysis Summary</div>',
        unsafe_allow_html=True
    )


    summary1, summary2, summary3 = st.columns(
        3
    )


    with summary1:

        st.metric(
            "Detected Plant",
            result["plant"]
        )


    with summary2:

        st.metric(
            "Predicted Disease",
            result["disease"]
        )


    with summary3:

        st.metric(
            "Model Confidence",
            f"{confidence_percentage:.2f}%"
        )
    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📄 Download Analysis Report</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Download a PDF summary of the PlantVision "
        "analysis, prediction results, and plant health guidance."
    )

    # Generate PDF
    pdf_report = generate_pdf_report(
        result,
        area_result,
        disease_details
    )

    # Safe filename
    plant_name = (
        result["plant"]
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
    )

    disease_name = (
        result["disease"]
        .replace(" ", "_")
        .replace("/", "_")
    )

    report_filename = (
        f"PlantVision_{plant_name}_{disease_name}_Report.pdf"
    )

    st.download_button(
        label="📄 Download PlantVision Report",
        data=pdf_report,
        file_name=report_filename,
        mime="application/pdf",
        type="primary",
        width="stretch"
    )

    st.caption(
        "The downloaded report contains the AI prediction, "
        "confidence score, visual-analysis estimate, "
        "plant health guidance, and important limitations."
    )

    # -----------------------------------------------------
    # ADDITIONAL SUMMARY
    # -----------------------------------------------------

    summary4, summary5 = st.columns(
        2
    )


    with summary4:

        st.metric(
            "Affected Area Estimate",
            f"{affected:.2f}%"
        )


    with summary5:

        st.metric(
            "Confidence Level",
            result["confidence_status"]
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
<div class="footer">

🌿 <b>PlantVision AI</b><br><br>

Deep Learning • Computer Vision • Explainable AI

<br><br>

Built for intelligent plant health analysis.

</div>
""",
    unsafe_allow_html=True
)