# model_utils.py
from transformers import AutoModelForImageClassification, AutoImageProcessor
from PIL import Image
import torch

# Path to your trained ViT model
MODEL_PATH = "./vit_leaf_model"

# Initialize processor and model
try:
    feature_extractor = AutoImageProcessor.from_pretrained(MODEL_PATH)
except:
    # Fallback if preprocessor_config.json is missing or old version
    from transformers import ViTImageProcessor
    feature_extractor = ViTImageProcessor(
        do_resize=True,
        size=224,
        do_normalize=True,
        image_mean=[0.5, 0.5, 0.5],
        image_std=[0.5, 0.5, 0.5]
    )

# Load your trained model
model = AutoModelForImageClassification.from_pretrained(MODEL_PATH)
model.eval()  # put model in eval mode

# GPU support
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Prediction function
def predict_leaf_disease(image: Image.Image):
    """
    Predict leaf disease from a PIL image.

    Args:
        image (PIL.Image.Image): Input leaf image

    Returns:
        dict: {'disease_name': str, 'confidence': float}
    """
    # Process the image
    inputs = feature_extractor(images=image, return_tensors="pt").to(device)

    # Forward pass
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred_id = torch.argmax(logits, dim=1).item()
        confidence = torch.softmax(logits, dim=1)[0, pred_id].item() * 100

    # Map class ID to label
    label = model.config.id2label[pred_id]

    return {"disease_name": label, "confidence": round(confidence, 2)}
