# 🪴 AI-Powered Leaf Disease Detection System

## Project Overview

Plant health is critical for agriculture, and early detection of leaf diseases can prevent significant crop losses. This project presents an AI-driven leaf disease detection system that integrates a fine-tuned Vision Transformer (ViT) model for disease classification with Groq API for detailed disease explanation and treatment recommendations. The system provides a robust pipeline for image preprocessing, disease prediction, severity assessment, and actionable advice, making it suitable for both research and practical applications in precision agriculture.

## Problem Statement

Crop diseases cause severe agricultural and economic losses worldwide. Traditional methods of disease identification are time-consuming, subjective, and require expert knowledge. There is a need for automated, accurate, and interpretable disease detection systems that can assist farmers and agronomists in early diagnosis and treatment planning.

## Objectives

- Develop an AI model capable of detecting multiple leaf diseases with high accuracy.
- Provide disease severity assessment to prioritize intervention.
- Generate interpretable outputs including symptoms, causes, and treatment recommendations using Groq API.
- Deploy the system via a Streamlit interface for ease of use by non-technical stakeholders.
- Optimize the system for low-latency inference suitable for field deployment.

## Dataset

### PlantVillage Dataset (BrandonFors/Plant-Diseases-PlantVillage-Dataset)

- Open-source dataset containing ~50,000 images of healthy and diseased plant leaves.
- Covers 38 classes across 14 crop types.
- Images vary in lighting, orientation, and background, providing realistic conditions for model training.
- Used train-test split (80%-20%) for model development.

### Dataset Preprocessing

- Images resized to 224x224 pixels for ViT input.
- Normalization applied based on ImageNet statistics.
- Optional dataset reduction or augmentation to optimize training time.

## Model Architecture

### Vision Transformer (ViT) - Hugging Face implementation

- Pre-trained on ImageNet, fine-tuned on PlantVillage dataset.
- Lightweight variant used for faster training and inference.
- Handles multi-class classification for leaf diseases.

### Fine-tuning Details

- **Loss function:** Cross-entropy
- **Optimizer:** AdamW
- **Learning rate scheduler** with warm-up
- **Evaluation metric:** Accuracy
- Batch size and epochs tuned for Colab/mobile training constraints

## Methodology

1. **Image Input:** Users upload leaf images (JPG, PNG, BMP, TIFF).
2. **Preprocessing:** Resize, normalize, and convert images to PyTorch tensors.
3. **Model Prediction:** Fine-tuned ViT predicts the disease class.
4. **Groq API Integration:** Sends model prediction for detailed disease explanation:
   - Symptoms
   - Possible causes
   - Treatment recommendations
   - Confidence score and severity level
5. **Output Formatting:** Structured JSON result for Streamlit interface.

### Example Output
```
🦠 Leaf Spot Disease (Cercospora leaf spot)
Type: fungal
Severity: moderate
Confidence: 90.0%

Symptoms
- Small, circular or oval spots on the leaf
- Spots are grayish-white with dark brown borders
- Yellowing of the leaf

Possible Causes
- Infection by the fungus Cercospora
- High humidity
- Poor air circulation

Treatment
- Remove infected leaves
- Improve air circulation
- Apply fungicides
```

## Project Structure
```
app/
│
├─ model/                     # Fine-tuned ViT model files
│   ├─ config.json
│   ├─ preprocessor_config.json
│   └─ model.safetensors
│
├─ model_utils.py             # Model loading and inference functions
├─ groq_utils.py              # Groq API integration for disease explanations
├─ utils.py                   # Image preprocessing & helper functions
├─ app.py                     # Streamlit interface for users
├─ .env                       # Environment variables (GROQ_API_KEY)
├─ requirements.txt           # Python dependencies
└─ Media/                     # Sample leaf images for testing
```

## Implementation Highlights

- **Multi-modal pipeline:** Combines deep learning predictions with expert knowledge via Groq API.
- **Optimized for performance:** Reduced dataset, lightweight ViT, batch inference, and preprocessed images for fast predictions.
- **Streamlit frontend:** Simple drag-and-drop interface with real-time predictions.
- **Scalable:** Can integrate additional disease datasets or crop types.
- **Explainable AI:** Outputs interpretable results with symptoms, causes, and treatments for actionable insights.

## Evaluation Metrics

- **Accuracy:** 88-92% across fungal, bacterial, viral, and pest-related diseases
- **F1-Score:** Evaluated per class to handle class imbalance
- **Confidence scoring:** Probability-based scoring from ViT model
- **Latency:** ~2-5 seconds per image

## Future Work

- Add attention visualization to highlight diseased leaf areas.
- Support multi-leaf and batch image prediction.
- Expand Groq explanations with real-time recommendation ranking.
- Deploy a mobile-friendly interface for farmers in the field.

## Installation and Usage

1. Clone the repository:
```bash
   git clone <repo-url>
   cd app
```

2. Set up virtual environment and install dependencies:
```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   .\venv\Scripts\activate       # Windows
   pip install -r requirements.txt
```

3. Set environment variables in `.env`:
```
   GROQ_API_KEY=your_groq_api_key
```

4. Launch the Streamlit app:
```bash
   streamlit run app.py
```

5. Upload a leaf image and view disease predictions with explanations.

## References

- **PlantVillage Dataset:** https://www.kaggle.com/datasets/brandondfors/plant-diseases-plantvillage-dataset
- **Hugging Face Vision Transformer:** https://huggingface.co/docs/transformers/model_doc/vit
- **Groq API Documentation:** https://docs.groq.com
