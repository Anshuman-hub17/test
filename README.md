# 🌿 PlantVision AI

### AI-Powered Plant Disease Detection & Explainable Leaf Analysis

PlantVision AI is an end-to-end deep learning web application designed to identify plant diseases from leaf images and provide interpretable visual analysis.

The system combines **Deep Learning, Computer Vision, Explainable AI, FastAPI, and a custom web interface** to provide disease predictions, confidence scores, visual abnormality estimation, Grad-CAM attention maps, plant-health guidance, and downloadable PDF reports.

---

## 🚀 Live Demo

🌐 **PlantVision AI:**  
https://plantvision-ai-k2dq.onrender.com

> ⚠️ The application is hosted on a free cloud instance. The first request may take some time if the server has been inactive.

---

## ✨ Key Features

- 🌿 Automatic plant identification
- 🦠 AI-based plant disease classification
- 🧠 MobileNetV2 deep learning architecture
- 📊 Prediction confidence score
- 🏆 Top-3 prediction ranking
- 🔬 Computer-vision leaf region detection
- 🦠 Visual abnormality estimation
- 🔥 Grad-CAM explainable AI visualization
- 🌱 Disease-specific plant health guidance
- 📋 Complete analysis summary
- 📄 Downloadable PDF analysis report
- ⚡ FastAPI-powered backend
- 🎨 Responsive HTML, CSS and JavaScript frontend
- ☁️ Cloud deployment using Render

---

## 🌱 Supported Plants

PlantVision currently supports disease analysis for:

- 🍎 Apple
- 🌽 Corn (Maize)
- 🍇 Grape
- 🫑 Bell Pepper
- 🥔 Potato
- 🍅 Tomato

The trained model contains **27 classification classes** across supported plants and disease conditions.

---

## 🧠 AI Model

| Component | Technology |
|---|---|
| Architecture | MobileNetV2 |
| Framework | TensorFlow / Keras |
| Input | Plant leaf image |
| Image Size | 224 × 224 |
| Number of Classes | 27 |
| Explainability | Grad-CAM |
| Image Analysis | OpenCV |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |

MobileNetV2 was selected as the primary classification architecture because its lightweight convolutional architecture provides a good balance between predictive capability and deployment efficiency.

---

## 🔄 How PlantVision Works

```text
                 Leaf Image
                     │
                     ▼
              Image Upload
                     │
                     ▼
                 FastAPI
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
     MobileNetV2            OpenCV
          │                     │
          ▼                     ▼
 Disease Classification    Leaf Analysis
          │                     │
          ├─────────────┐       │
          │             │       │
          ▼             ▼       ▼
     Confidence       Grad-CAM  Abnormal
       Score          Analysis   Regions
          │             │       │
          └─────────────┴───────┘
                        │
                        ▼
                Plant Health Guidance
                        │
                        ▼
                  Analysis Summary
                        │
                        ▼
                   PDF Report
```

---

## 🔥 Explainable AI — Grad-CAM

PlantVision incorporates **Gradient-weighted Class Activation Mapping (Grad-CAM)** to improve model interpretability.

Instead of displaying only a disease prediction, Grad-CAM generates an attention heatmap showing the image regions that influenced the neural network's decision.

### Grad-CAM Output

PlantVision displays:

- Original uploaded leaf
- AI attention heatmap
- Grad-CAM overlay

Warmer regions indicate areas receiving stronger model attention.

> Grad-CAM represents model attention and should not be interpreted as an independent biological identification of diseased tissue.

---

## 🔬 Visual Leaf Analysis

In addition to deep-learning classification, PlantVision uses **OpenCV-based computer vision** to analyze visible leaf regions.

The analysis pipeline performs:

1. Image resizing and preprocessing
2. RGB-to-HSV conversion
3. Green leaf-region segmentation
4. Yellow/brown region detection
5. Dark-region detection
6. Morphological noise reduction
7. Abnormal-region estimation
8. Estimated visually affected-area calculation

The application displays:

- Original leaf
- Detected leaf region
- Visually abnormal regions
- Estimated visually affected area

> The affected-area percentage is based on image color and region analysis and is not an exact biological disease-severity measurement.

---

## 🌱 Plant Health Guidance

After disease detection, PlantVision provides educational information related to the predicted condition.

The guidance includes:

- 📖 About the disease
- 👁️ Common visual signs
- 🛠️ Suggested next steps
- 🛡️ Prevention information

The recommendations are intended for educational support and should not replace professional agricultural diagnosis.

---

## 📄 PDF Analysis Report

PlantVision can generate a downloadable PDF report containing the analysis results.

The report includes information such as:

- Detected plant
- Predicted disease
- Prediction confidence
- Visual analysis estimate
- Plant-health guidance
- Analysis limitations

This allows users to save or share their PlantVision analysis.

---

## 🛠️ Technology Stack

### Machine Learning & AI

- Python
- TensorFlow
- Keras
- MobileNetV2
- NumPy
- Grad-CAM

### Computer Vision

- OpenCV
- Pillow
- HSV image segmentation
- Morphological image processing

### Backend

- FastAPI
- Uvicorn
- Python Multipart

### Frontend

- HTML5
- CSS3
- JavaScript

### Report Generation

- ReportLab

### Development & Deployment

- Git
- GitHub
- Render
- VS Code

---

## 📁 Project Structure

```text
PlantVision-AI/
│
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── disease_info.py
│   ├── gradcam.py
│   ├── image_analysis.py
│   ├── predictor.py
│   ├── report_generator.py
│   └── utils.py
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── models/
│   ├── class_names.pkl
│   └── plantvision_mobilenet_finetuned.keras
│
├── notebooks/
│   ├── 01_dataset_analysis.ipynb
│   └── 02_deep_learning.ipynb
│
├── requirements.txt
├── test_predictor.py
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/aditya44-git/PlantVision-AI.git
```

Move into the project:

```bash
cd PlantVision-AI
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv-dl
```

Activate it:

```bash
.venv-dl\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI application

```bash
python -m uvicorn backend.main:app --reload
```

### 5. Open PlantVision

Open:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 🖼️ Using PlantVision

1. Open the PlantVision web application.
2. Upload a clear JPG, JPEG, or PNG leaf image.
3. Keep the leaf clearly visible and well-lit.
4. Start the AI analysis.
5. Review the detected plant and predicted condition.
6. Check the prediction confidence and Top-3 predictions.
7. Examine the visual abnormality analysis.
8. Inspect the Grad-CAM attention visualization.
9. Read the plant-health guidance.
10. Download the PDF analysis report if required.

---

## 📊 Model Output

For every uploaded image, the classification pipeline produces:

```text
Detected Plant
Predicted Disease
Prediction Confidence
Top-3 Predictions
```

The results are supplemented with computer-vision analysis and explainability information to provide more context than a simple classification output.

---

## ⚠️ Limitations

PlantVision AI has several important limitations:

- Predictions depend heavily on image quality.
- Only supported plant species should be analyzed.
- Similar-looking diseases may be difficult for the model to distinguish.
- Real-world environmental conditions can differ from training data.
- Grad-CAM identifies model attention rather than confirmed diseased tissue.
- The affected-area estimate is based on visual image processing.
- Disease severity is not clinically or biologically measured by the system.
- AI predictions should be verified when important agricultural decisions are involved.

---

## 🔮 Future Improvements

Potential future developments include:

- Support for additional crop species
- Larger real-world disease datasets
- Improved disease severity estimation
- Object detection/localization of individual lesions
- Field-image support with complex backgrounds
- Multilingual plant-health guidance
- User diagnosis history
- Mobile application integration
- Agricultural expert verification
- Location-aware disease recommendations

---

## 🎯 Project Objective

The objective of PlantVision AI is to demonstrate how multiple AI technologies can be integrated into a complete, deployable application rather than building only a standalone prediction model.

The project combines:

**Deep Learning + Computer Vision + Explainable AI + Backend Development + Frontend Development + Cloud Deployment**

to create an end-to-end intelligent plant-health analysis system.

---

## ⚠️ Disclaimer

PlantVision AI is an **AI-based educational and analysis tool**.

Predictions, visual analysis, and plant-health guidance should not be considered a substitute for professional agricultural diagnosis. Disease appearance and appropriate management can vary depending on crop variety, climate, location, growing conditions, and disease severity.

For serious or rapidly spreading crop problems, consult a qualified agricultural professional.

---

## 👨‍💻 Author

**Aditya Kumar Rath**

B.Tech — Computer Science & Engineering (AI & ML)

Interested in:

- Artificial Intelligence
- Machine Learning
- Data Science
- Computer Vision
- Full-Stack AI Applications

---

## ⭐ Support

If you find PlantVision AI useful or interesting, consider giving the repository a ⭐ on GitHub.

---

### 🌿 PlantVision AI

**Deep Learning • Computer Vision • Explainable AI**

Built for intelligent plant health analysis.