// =========================================================
// PLANTVISION AI FRONTEND
// =========================================================

const API_URL = "";


// =========================================================
// ELEMENTS
// =========================================================

const uploadBox = document.getElementById("uploadBox");
const leafInput = document.getElementById("leafInput");
const browseButton = document.getElementById("browseButton");

const selectedFile = document.getElementById("selectedFile");
const fileName = document.getElementById("fileName");
const removeFile = document.getElementById("removeFile");

const analyzeButton = document.getElementById("analyzeButton");

const emptyState = document.getElementById("emptyState");
const tipsCard = document.getElementById("tipsCard");

const loadingState = document.getElementById("loadingState");
const errorMessage = document.getElementById("errorMessage");

const resultsContainer = document.getElementById("resultsContainer");

const uploadedPreview = document.getElementById("uploadedPreview");
const visualOriginal = document.getElementById("visualOriginal");
const gradOriginal = document.getElementById("gradOriginal");

const downloadReportButton =
    document.getElementById("downloadReportButton");

let currentFile = null;


// =========================================================
// BROWSE FILE
// =========================================================

browseButton.addEventListener("click", (event) => {

    event.stopPropagation();
    leafInput.click();

});


uploadBox.addEventListener("click", () => {

    leafInput.click();

});


leafInput.addEventListener("change", () => {

    if (leafInput.files.length > 0) {

        handleFile(
            leafInput.files[0]
        );

    }

});


// =========================================================
// DRAG AND DROP
// =========================================================

uploadBox.addEventListener("dragover", (event) => {

    event.preventDefault();

    uploadBox.classList.add(
        "dragging"
    );

});


uploadBox.addEventListener("dragleave", () => {

    uploadBox.classList.remove(
        "dragging"
    );

});


uploadBox.addEventListener("drop", (event) => {

    event.preventDefault();

    uploadBox.classList.remove(
        "dragging"
    );


    if (event.dataTransfer.files.length > 0) {

        handleFile(
            event.dataTransfer.files[0]
        );

    }

});


// =========================================================
// SELECT FILE
// =========================================================

function handleFile(file) {

    const allowedTypes = [
        "image/jpeg",
        "image/png"
    ];


    if (!allowedTypes.includes(file.type)) {

        showError(
            "Please upload a JPG, JPEG or PNG image."
        );

        return;

    }


    currentFile = file;

    fileName.textContent = file.name;


    selectedFile.classList.remove(
        "hidden"
    );

    analyzeButton.classList.remove(
        "hidden"
    );


    emptyState.classList.add(
        "hidden"
    );

    tipsCard.classList.add(
        "hidden"
    );

    errorMessage.classList.add(
        "hidden"
    );

    resultsContainer.classList.add(
        "hidden"
    );


    // -----------------------------------------------------
    // IMAGE PREVIEW
    // -----------------------------------------------------

    const reader = new FileReader();


    reader.onload = (event) => {

        uploadedPreview.src =
            event.target.result;

        visualOriginal.src =
            event.target.result;

        gradOriginal.src =
            event.target.result;

    };


    reader.readAsDataURL(file);

}


// =========================================================
// REMOVE FILE
// =========================================================

removeFile.addEventListener("click", () => {

    currentFile = null;

    leafInput.value = "";


    selectedFile.classList.add(
        "hidden"
    );

    analyzeButton.classList.add(
        "hidden"
    );

    resultsContainer.classList.add(
        "hidden"
    );


    emptyState.classList.remove(
        "hidden"
    );

    tipsCard.classList.remove(
        "hidden"
    );


    errorMessage.classList.add(
        "hidden"
    );

});


// =========================================================
// ANALYZE
// =========================================================

analyzeButton.addEventListener(
    "click",
    async () => {

        if (!currentFile) {

            showError(
                "Please select a leaf image first."
            );

            return;

        }


        loadingState.classList.remove(
            "hidden"
        );

        errorMessage.classList.add(
            "hidden"
        );

        resultsContainer.classList.add(
            "hidden"
        );


        analyzeButton.disabled = true;

        analyzeButton.textContent =
            "Analyzing...";


        try {

            const formData =
                new FormData();


            formData.append(
                "file",
                currentFile
            );


            const response = await fetch(
                `${API_URL}/predict`,
                {
                    method: "POST",
                    body: formData
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "PlantVision analysis failed."
                );

            }


            displayResults(
                data
            );

        }

        catch (error) {

            showError(
                error.message
            );

        }

        finally {

            loadingState.classList.add(
                "hidden"
            );


            analyzeButton.disabled = false;

            analyzeButton.textContent =
                "🌿 Analyze Leaf";

        }

    }
);


// =========================================================
// DISPLAY RESULTS
// =========================================================

function displayResults(data) {

    const prediction =
        data.prediction;

    const visualAnalysis =
        data.visual_analysis;

    const gradcam =
        data.gradcam;

    const guidance =
        data.health_guidance;


    // =====================================================
    // DIAGNOSIS
    // =====================================================

    document.getElementById(
        "plantValue"
    ).textContent =
        prediction.plant;


    document.getElementById(
        "diseaseValue"
    ).textContent =
        prediction.disease;


    document.getElementById(
        "confidenceValue"
    ).textContent =
        `${Number(
            prediction.confidence
        ).toFixed(2)}%`;


    // =====================================================
    // CONFIDENCE MESSAGE
    // =====================================================

    const confidenceMessage =
        document.getElementById(
            "confidenceMessage"
        );


    confidenceMessage.textContent =
        prediction.message;


    confidenceMessage.className =
        "status-message";


    const status =
        String(
            prediction.confidence_status
        ).toLowerCase();


    if (status === "high") {

        confidenceMessage.classList.add(
            "status-high"
        );

    }

    else if (status === "moderate") {

        confidenceMessage.classList.add(
            "status-moderate"
        );

    }

    else {

        confidenceMessage.classList.add(
            "status-low"
        );

    }


    // =====================================================
    // TOP 3
    // =====================================================

    displayTopPredictions(
        data.top_predictions
    );


    // =====================================================
    // ORIGINAL IMAGE
    // =====================================================

    if (visualAnalysis.original_image) {

        visualOriginal.src =
            visualAnalysis.original_image;

        gradOriginal.src =
            visualAnalysis.original_image;

    }


    // =====================================================
    // LEAF MASK
    // =====================================================

    showAnalysisImage(
        "leafMaskPlaceholder",
        visualAnalysis.leaf_mask,
        "Detected Leaf Region"
    );


    // =====================================================
    // AFFECTED MASK
    // =====================================================

    showAnalysisImage(
        "affectedMaskPlaceholder",
        visualAnalysis.affected_mask,
        "Visually Abnormal Regions"
    );


    // =====================================================
    // GRAD-CAM HEATMAP
    // =====================================================

    showAnalysisImage(
        "heatmapPlaceholder",
        gradcam.heatmap,
        "AI Attention Heatmap"
    );


    // =====================================================
    // GRAD-CAM OVERLAY
    // =====================================================

    showAnalysisImage(
        "overlayPlaceholder",
        gradcam.overlay,
        "Grad-CAM Overlay"
    );


    // =====================================================
    // AFFECTED AREA
    // =====================================================

    document.getElementById(
        "affectedAreaValue"
    ).textContent =
        `${Number(
            visualAnalysis.affected_percentage
        ).toFixed(2)}%`;


    // =====================================================
    // GUIDANCE
    // =====================================================

    displayGuidance(
        guidance,
        prediction
    );


    // =====================================================
    // SUMMARY
    // =====================================================

    document.getElementById(
        "summaryPlant"
    ).textContent =
        prediction.plant;


    document.getElementById(
        "summaryDisease"
    ).textContent =
        prediction.disease;


    document.getElementById(
        "summaryConfidence"
    ).textContent =
        `${Number(
            prediction.confidence
        ).toFixed(2)}%`;


    document.getElementById(
        "summaryAffected"
    ).textContent =
        `${Number(
            visualAnalysis.affected_percentage
        ).toFixed(2)}%`;


    document.getElementById(
        "summaryStatus"
    ).textContent =
        prediction.confidence_status;


    // =====================================================
    // SHOW RESULTS
    // =====================================================

    resultsContainer.classList.remove(
        "hidden"
    );


    resultsContainer.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


// =========================================================
// DISPLAY ANALYSIS IMAGE
// =========================================================

function showAnalysisImage(
    containerId,
    imageSource,
    altText
) {

    const container =
        document.getElementById(
            containerId
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    if (!imageSource) {

        container.textContent =
            "Image unavailable.";

        return;

    }


    const image =
        document.createElement("img");


    image.src =
        imageSource;

    image.alt =
        altText;


    image.style.width =
        "100%";

    image.style.height =
        "100%";

    image.style.objectFit =
        "contain";

    image.style.display =
        "block";


    container.appendChild(
        image
    );

}


// =========================================================
// TOP PREDICTIONS
// =========================================================

function displayTopPredictions(
    predictions
) {

    const predictionGrid =
        document.getElementById(
            "predictionGrid"
        );


    predictionGrid.innerHTML = "";


    predictions.forEach(
        (prediction, index) => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "prediction-card";


            const confidence =
                Number(
                    prediction.confidence
                );


            card.innerHTML = `

                <div class="prediction-rank">
                    #${index + 1}
                </div>

                <div class="prediction-name">
                    ${escapeHTML(
                        prediction.plant
                    )}
                </div>

                <div class="prediction-disease">
                    ${escapeHTML(
                        prediction.disease
                    )}
                </div>

                <div class="progress-track">

                    <div
                        class="progress-fill"
                        style="width:
                        ${Math.min(
                            confidence,
                            100
                        )}%"
                    ></div>

                </div>

                <div class="prediction-confidence">

                    ${confidence.toFixed(2)}%
                    confidence

                </div>

            `;


            predictionGrid.appendChild(
                card
            );

        }
    );

}


// =========================================================
// GUIDANCE
// =========================================================

function displayGuidance(
    guidance,
    prediction
) {

    const conditionStatus =
        document.getElementById(
            "conditionStatus"
        );


    if (guidance.healthy) {

        conditionStatus.textContent =
            "🌿 The model classified this leaf as healthy.";

        conditionStatus.className =
            "condition-status status-high";

    }

    else {

        conditionStatus.textContent =
            `🦠 Predicted condition: ${prediction.disease}`;

        conditionStatus.className =
            "condition-status status-moderate";

    }


    document.getElementById(
        "aboutText"
    ).textContent =
        guidance.about || "";


    populateList(
        "symptomsList",
        guidance.common_visual_signs
    );


    populateList(
        "actionsList",
        guidance.suggested_next_steps
    );


    populateList(
        "preventionList",
        guidance.prevention
    );

}


// =========================================================
// POPULATE LIST
// =========================================================

function populateList(
    elementId,
    items
) {

    const element =
        document.getElementById(
            elementId
        );


    element.innerHTML = "";


    if (
        !Array.isArray(items) ||
        items.length === 0
    ) {

        const li =
            document.createElement(
                "li"
            );


        li.textContent =
            "No additional information available.";


        element.appendChild(
            li
        );

        return;

    }


    items.forEach((item) => {

        const li =
            document.createElement(
                "li"
            );


        li.textContent =
            item;


        element.appendChild(
            li
        );

    });

}


// =========================================================
// PDF DOWNLOAD
// =========================================================

downloadReportButton.addEventListener(
    "click",
    async () => {

        if (!currentFile) {

            showError(
                "Please analyze a leaf before downloading the report."
            );

            return;

        }


        const originalButtonText =
            downloadReportButton.textContent;


        downloadReportButton.disabled =
            true;


        downloadReportButton.textContent =
            "Generating PDF...";


        try {

            const formData =
                new FormData();


            formData.append(
                "file",
                currentFile
            );


            const response = await fetch(
                `${API_URL}/report`,
                {
                    method: "POST",
                    body: formData
                }
            );


            if (!response.ok) {

                let message =
                    "Could not generate the PDF report.";


                try {

                    const errorData =
                        await response.json();


                    if (errorData.detail) {

                        message =
                            errorData.detail;

                    }

                }

                catch (_) {
                    // Ignore JSON parsing failure.
                }


                throw new Error(
                    message
                );

            }


            // -------------------------------------------------
            // PDF BLOB
            // -------------------------------------------------

            const pdfBlob =
                await response.blob();


            const downloadURL =
                URL.createObjectURL(
                    pdfBlob
                );


            // -------------------------------------------------
            // TEMPORARY DOWNLOAD LINK
            // -------------------------------------------------

            const link =
                document.createElement(
                    "a"
                );


            link.href =
                downloadURL;


            link.download =
                "PlantVision_Analysis_Report.pdf";


            document.body.appendChild(
                link
            );


            link.click();


            document.body.removeChild(
                link
            );


            URL.revokeObjectURL(
                downloadURL
            );

        }

        catch (error) {

            showError(
                error.message
            );

        }

        finally {

            downloadReportButton.disabled =
                false;


            downloadReportButton.textContent =
                originalButtonText;

        }

    }
);


// =========================================================
// ERROR
// =========================================================

function showError(message) {

    errorMessage.textContent =
        `⚠️ ${message}`;


    errorMessage.classList.remove(
        "hidden"
    );

}


// =========================================================
// BASIC HTML ESCAPING
// =========================================================

function escapeHTML(value) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        value ?? "";


    return div.innerHTML;

}