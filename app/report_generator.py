from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


def generate_pdf_report(
    result,
    area_result,
    disease_details
):
    """
    Generate a PlantVision AI analysis report
    and return the PDF as bytes.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm
    )

    styles = getSampleStyleSheet()

    # =====================================================
    # CUSTOM STYLES
    # =====================================================

    title_style = ParagraphStyle(
        "PlantVisionTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "PlantVisionSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        "PlantVisionSection",
        parent=styles["Heading2"],
        fontSize=15,
        leading=19,
        spaceBefore=14,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "PlantVisionBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=16,
        spaceAfter=6
    )

    small_style = ParagraphStyle(
        "PlantVisionSmall",
        parent=styles["BodyText"],
        fontSize=8,
        leading=12,
        textColor=colors.grey
    )

    story = []

    # =====================================================
    # HEADER
    # =====================================================

    story.append(
        Paragraph(
            "PlantVision AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Plant Disease Analysis Report",
            subtitle_style
        )
    )

    generated_time = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    story.append(
        Paragraph(
            f"<b>Report generated:</b> {generated_time}",
            body_style
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # =====================================================
    # AI DIAGNOSIS
    # =====================================================

    story.append(
        Paragraph(
            "AI Diagnosis",
            section_style
        )
    )

    confidence = (
        result["confidence"] * 100
    )

    diagnosis_data = [
        [
            "Detected Plant",
            str(result["plant"])
        ],
        [
            "Predicted Condition",
            str(result["disease"])
        ],
        [
            "Prediction Confidence",
            f"{confidence:.2f}%"
        ],
        [
            "Confidence Level",
            str(result["confidence_status"])
        ]
    ]

    diagnosis_table = Table(
        diagnosis_data,
        colWidths=[
            6 * cm,
            10 * cm
        ]
    )

    diagnosis_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#E8F5E9")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.black
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#BDBDBD")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    story.append(
        diagnosis_table
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            f"<b>Model message:</b> {result['message']}",
            body_style
        )
    )

    # =====================================================
    # TOP 3 PREDICTIONS
    # =====================================================

    story.append(
        Paragraph(
            "Top Predictions",
            section_style
        )
    )

    top_data = [
        [
            "Rank",
            "Plant",
            "Condition",
            "Confidence"
        ]
    ]

    for rank, prediction in enumerate(
        result["top_predictions"],
        start=1
    ):

        top_data.append(
            [
                str(rank),
                str(prediction["plant"]),
                str(prediction["disease"]),
                (
                    f"{prediction['confidence'] * 100:.2f}%"
                )
            ]
        )

    top_table = Table(
        top_data,
        colWidths=[
            1.5 * cm,
            4 * cm,
            7 * cm,
            3.5 * cm
        ],
        repeatRows=1
    )

    top_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2E7D32")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#BDBDBD")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    story.append(
        top_table
    )

    # =====================================================
    # VISUAL ANALYSIS
    # =====================================================

    story.append(
        Paragraph(
            "Visual Leaf Analysis",
            section_style
        )
    )

    affected_percentage = area_result[
        "affected_percentage"
    ]

    story.append(
        Paragraph(
            (
                "<b>Estimated visually affected area:</b> "
                f"{affected_percentage:.2f}%"
            ),
            body_style
        )
    )

    story.append(
        Paragraph(
            (
                "The affected-area percentage is estimated "
                "using image color and region analysis. "
                "It is not an exact biological measurement "
                "of disease severity."
            ),
            small_style
        )
    )

    # =====================================================
    # PLANT HEALTH INFORMATION
    # =====================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "Plant Health Guidance",
            section_style
        )
    )

    if disease_details["healthy"]:

        story.append(
            Paragraph(
                (
                    "<b>Status:</b> The model classified "
                    "the uploaded leaf as healthy."
                ),
                body_style
            )
        )

    else:

        story.append(
            Paragraph(
                (
                    "<b>Predicted condition:</b> "
                    f"{result['disease']}"
                ),
                body_style
            )
        )

    # ABOUT
    story.append(
        Paragraph(
            "About",
            section_style
        )
    )

    story.append(
        Paragraph(
            disease_details["about"],
            body_style
        )
    )

    # SYMPTOMS
    if disease_details["symptoms"]:

        story.append(
            Paragraph(
                "Common Visual Signs",
                section_style
            )
        )

        for symptom in disease_details[
            "symptoms"
        ]:

            story.append(
                Paragraph(
                    f"• {symptom}",
                    body_style
                )
            )

    # ACTIONS
    story.append(
        Paragraph(
            "Suggested Next Steps",
            section_style
        )
    )

    for action in disease_details[
        "actions"
    ]:

        story.append(
            Paragraph(
                f"• {action}",
                body_style
            )
        )

    # PREVENTION
    story.append(
        Paragraph(
            "Prevention",
            section_style
        )
    )

    for prevention in disease_details[
        "prevention"
    ]:

        story.append(
            Paragraph(
                f"• {prevention}",
                body_style
            )
        )

    # =====================================================
    # DISCLAIMER
    # =====================================================

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Important Notice",
            section_style
        )
    )

    story.append(
        Paragraph(
            (
                "PlantVision AI provides automated image-based "
                "analysis and general educational information. "
                "Predictions can be incorrect, especially when "
                "model confidence is low or the uploaded image "
                "differs from the training data. This report "
                "should not replace professional agricultural "
                "diagnosis or locally appropriate crop-management "
                "advice."
            ),
            small_style
        )
    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    document.build(
        story
    )

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes