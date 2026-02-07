import streamlit as st
from PIL import Image
from model_utils import predict_leaf_disease
from groq_utils import get_disease_info

# Page configuration
st.set_page_config(
    page_title="🌿 Leaf Disease Detector",
    layout="wide"
)

# Minimal and clean CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #fafaf9;
    }
    
    .main-header {
        text-align: center;
        padding: 2em 1em 1.5em 1em;
        background: white;
        border-radius: 16px;
        margin-bottom: 2em;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #e7e5e4;
    }
    
    .header-icon {
        font-size: 2.5em;
        margin-bottom: 0.2em;
    }
    
    .main-title {
        color: #0a0a0a !important;
        font-size: 2em !important;
        font-weight: 600 !important;
        margin: 0.2em 0 0.3em 0 !important;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #3f3f46 !important;
        font-size: 1em !important;
        font-weight: 400 !important;
        margin: 0 !important;
    }
    
    .upload-card {
        background: white;
        border-radius: 16px;
        padding: 2em;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #e7e5e4;
        height: 100%;
    }
    
    .upload-card h3 {
        color: #0a0a0a !important;
        font-weight: 600 !important;
    }
    
    .result-card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        padding: 2em;
        margin-bottom: 1.5em;
        border: 1px solid #e7e5e4;
    }
    
    .disease-title {
        font-size: 1.8em;
        font-weight: 600;
        margin-bottom: 0.8em;
        color: #0a0a0a;
        padding-bottom: 0.5em;
        border-bottom: 3px solid #78716c;
    }
    
    .info-row {
        display: flex;
        gap: 1em;
        margin: 1.2em 0;
        flex-wrap: wrap;
    }
    
    .info-badge {
        background: #fafaf9;
        border: 1px solid #d6d3d1;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 0.95em;
        color: #18181b;
    }
    
    .info-badge strong {
        color: #0a0a0a;
        font-weight: 600;
    }
    
    .section-title {
        color: #0a0a0a;
        font-size: 1.2em;
        font-weight: 600;
        margin: 1.5em 0 0.8em 0;
        padding-bottom: 0.5em;
        border-bottom: 2px solid #e7e5e4;
    }
    
    .content-box {
        background: #fafaf9;
        border-radius: 8px;
        padding: 1.2em;
        margin: 1em 0;
        border: 1px solid #e7e5e4;
    }
    
    .content-item {
        padding: 0.6em 0 0.6em 1.8em;
        position: relative;
        color: #18181b;
        font-size: 0.98em;
        line-height: 1.7;
        font-weight: 400;
    }
    
    .content-item::before {
        content: '•';
        position: absolute;
        left: 0.5em;
        color: #78716c;
        font-size: 1.5em;
        line-height: 0.8;
    }
    
    .project-info {
        background: #f5f5f4;
        border-radius: 16px;
        padding: 2em;
        margin-bottom: 2em;
        border: 1px solid #d6d3d1;
    }
    
    .project-title {
        color: #0a0a0a;
        font-size: 1.4em;
        font-weight: 600;
        margin-bottom: 0.8em;
    }
    
    .project-desc {
        color: #18181b;
        font-size: 1em;
        line-height: 1.8;
        margin-bottom: 1em;
    }
    
    .feature-list {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.8em;
        margin-top: 1em;
    }
    
    .feature-item {
        color: #27272a;
        font-size: 0.95em;
        padding: 0.6em;
        display: flex;
        align-items: center;
        gap: 0.5em;
        font-weight: 500;
    }
    
    .stButton > button {
        background: #78716c;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75em 2em;
        font-size: 1em;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
        margin-top: 1em;
    }
    
    .stButton > button:hover {
        background: #57534e;
        box-shadow: 0 4px 12px rgba(87,83,78,0.3);
    }
    
    /* Image styling */
    .stImage {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* ========== FILE UPLOADER STYLING - COMPLETE FIX ========== */
    
    /* Main container */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #a8a29e;
        border-radius: 12px;
        padding: 2em;
        text-align: center;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #78716c;
    }
    
    /* Remove inner borders */
    [data-testid="stFileUploader"] section {
        border: none !important;
        background: transparent !important;
    }
    
    /* Main label "Choose a leaf image" */
    [data-testid="stFileUploader"] label {
        color: #0a0a0a !important;
        font-weight: 600 !important;
        font-size: 1.05em !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* "Drag and drop file here" text */
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p {
        color: #0a0a0a !important;
        font-size: 1em !important;
        font-weight: 500 !important;
        visibility: visible !important;
        opacity: 1 !important;
        display: block !important;
    }
    
    /* File limit text */
    [data-testid="stFileUploader"] small {
        color: #52525b !important;
        font-size: 0.85em !important;
        visibility: visible !important;
        opacity: 1 !important;
        display: block !important;
        margin-top: 0.5em;
    }
    
    /* All text inside file uploader */
    [data-testid="stFileUploader"] * {
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Icons (cloud, document) */
    [data-testid="stFileUploader"] svg {
        fill: #78716c !important;
        opacity: 0.7 !important;
        width: 48px !important;
        height: 48px !important;
        margin-bottom: 1em;
    }
    
    /* Browse files button */
    [data-testid="stFileUploader"] button[kind="secondary"] {
        background: #78716c !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6em 1.8em !important;
        font-weight: 500 !important;
        font-size: 0.95em !important;
        margin-top: 1em !important;
    }
    
    [data-testid="stFileUploader"] button[kind="secondary"]:hover {
        background: #57534e !important;
    }
    
    /* All paragraphs and spans */
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span {
        color: #0a0a0a !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='main-header'>
        <div class='header-icon'>🌿</div>
        <h1 class='main-title'>Leaf Disease Detector</h1>
        <p class='subtitle'>AI-powered plant health diagnosis and treatment recommendations</p>
    </div>
""", unsafe_allow_html=True)

# About Project Section
st.markdown("""
    <div class='project-info'>
        <div class='project-title'>📋 About This Project</div>
        <p class='project-desc'>
        AI-powered system detects plant leaf diseases, predicts their severity, and provides 
        actionable treatment recommendations. It integrates a fine-tuned Hugging Face ViT model with the Groq API 
        to deliver detailed explanations in an easy-to-read format.
        </p>
        <div class='feature-list'>
            <div class='feature-item'>✓ AI-Powered Leaf Disease Detection</div>
            <div class='feature-item'>✓ Real-time Disease Detection</div>
            <div class='feature-item'>✓ Fine-Tuned ViT Model (google/vit-base-patch16-224)</div>
            <div class='feature-item'>✓ High Accuracy Diagnosis</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 1.2], gap="large")

# Left Column - Upload Section
with col1:
    st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #0a0a0a; font-weight: 600; margin-bottom: 1em;'>📤 Upload Leaf Image</h3>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a leaf image",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear photo of a plant leaf"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("🔍 Detect Disease"):
            st.session_state['analyze'] = True
    
    st.markdown("</div>", unsafe_allow_html=True)

# Right Column - Results Section
with col2:
    if uploaded_file and st.session_state.get('analyze', False):
        with st.spinner("Analyzing leaf image..."):
            result = predict_leaf_disease(image)
            label = result["disease_name"]
            confidence = result["confidence"]
            disease_info = get_disease_info(label)

        # Display results
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='disease-title'>🦠 {label}</div>", unsafe_allow_html=True)
        
        # Info badges
        st.markdown("<div class='info-row'>", unsafe_allow_html=True)
        st.markdown(f"<div class='info-badge'><strong>Type:</strong> {disease_info['disease_type']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='info-badge'><strong>Severity:</strong> {disease_info['severity']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='info-badge'><strong>Confidence:</strong> {confidence}%</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Symptoms
        st.markdown("<div class='section-title'>Symptoms</div>", unsafe_allow_html=True)
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        for s in disease_info['symptoms']:
            st.markdown(f"<div class='content-item'>{s}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Possible Causes
        st.markdown("<div class='section-title'>Possible Causes</div>", unsafe_allow_html=True)
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        for c in disease_info['possible_causes']:
            st.markdown(f"<div class='content-item'>{c}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Treatment
        st.markdown("<div class='section-title'>Treatment</div>", unsafe_allow_html=True)
        st.markdown("<div class='content-box'>", unsafe_allow_html=True)
        for t in disease_info['treatment']:
            st.markdown(f"<div class='content-item'>{t}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='result-card'>
                <div class='disease-title'>👋 Welcome</div>
                <p style='color: #18181b; line-height: 1.8; font-size: 1.05em; font-weight: 400;'>
                    Upload a leaf image to detect diseases and receive expert treatment recommendations.
                </p>
                <div class='section-title'>How It Works</div>
                <div class='content-box'>
                    <div class='content-item'>Upload a clear image of the affected leaf</div>
                    <div class='content-item'>Our AI analyzes the image for disease symptoms</div>
                    <div class='content-item'>Get instant diagnosis with confidence score</div>
                    <div class='content-item'>Receive detailed treatment recommendations</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; color: #3f3f46; font-size: 0.95em; padding: 2em 0; margin-top: 2em; font-weight: 500;'>
        Powered by AI • Helping maintain healthy plants worldwide 🌍
    </div>
""", unsafe_allow_html=True)