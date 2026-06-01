import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os
import time

st.set_page_config(page_title="WheelScan", page_icon="🛞", layout="wide", initial_sidebar_state="collapsed")

# ==================== CUSTOM CSS PREMIUM ====================
st.markdown("""
<style>
    /* Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .stApp {
        background: #09090B;
    }
    
    /* Custom container */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Navbar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(9, 9, 11, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #27272A;
        position: sticky;
        top: 0;
        z-index: 1000;
        margin-bottom: 2rem;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-icon {
        font-size: 1.8rem;
    }
    
    .logo-text {
        font-size: 1.25rem;
        font-weight: 600;
        background: linear-gradient(135deg, #A78BFA 0%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        color: #A1A1AA;
        font-size: 0.875rem;
    }
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 2rem 4rem;
        background: linear-gradient(180deg, #09090B 0%, #18181B 100%);
        border-radius: 32px;
        margin-bottom: 3rem;
        border: 1px solid #27272A;
    }
    
    .hero-badge {
        display: inline-block;
        background: #18181B;
        border: 1px solid #3F3F46;
        border-radius: 100px;
        padding: 0.25rem 1rem;
        font-size: 0.75rem;
        color: #A78BFA;
        margin-bottom: 1.5rem;
    }
    
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .hero p {
        color: #A1A1AA;
        font-size: 1.125rem;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Upload card */
    .upload-card {
        background: #18181B;
        border-radius: 24px;
        border: 1px solid #27272A;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .upload-card:hover {
        border-color: #3F3F46;
        background: #1F1F23;
    }
    
    .upload-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Result card */
    .result-card {
        background: #18181B;
        border-radius: 24px;
        border: 1px solid #27272A;
        overflow: hidden;
    }
    
    .result-header {
        padding: 1rem 1.5rem;
        background: #1F1F23;
        border-bottom: 1px solid #27272A;
        font-weight: 600;
        color: #FFFFFF;
    }
    
    /* Metric grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-item {
        background: #1F1F23;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #27272A;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #71717A;
        margin-top: 0.25rem;
    }
    
    /* Detection list */
    .detection-item {
        background: #1F1F23;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .status-healthy {
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.1);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .status-danger {
        background: rgba(239, 68, 68, 0.1);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    /* Recommendation box */
    .recommend-box {
        background: linear-gradient(135deg, #1F1F23 0%, #18181B 100%);
        border-radius: 16px;
        padding: 1.25rem;
        margin-top: 1rem;
        border: 1px solid #27272A;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #52525B;
        font-size: 0.75rem;
        border-top: 1px solid #27272A;
        margin-top: 3rem;
    }
    
    /* Hide Streamlit branding */
    .stFileUploader > div:first-child {
        background: transparent !important;
    }
    
    .stFileUploader > div:first-child > div {
        background: transparent !important;
    }
    
    button {
        background: linear-gradient(135deg, #A78BFA 0%, #60A5FA 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 100px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== NAVBAR ====================
st.markdown("""
<div class="navbar">
    <div class="logo">
        <span class="logo-icon">🛞</span>
        <span class="logo-text">WheelScan</span>
    </div>
    <div class="nav-links">
        <span>Dashboard</span>
        <span>About</span>
        <span>Documentation</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ==================== HERO ====================
st.markdown("""
<div class="hero">
    <div class="hero-badge">
        ⚡ AI-Powered Detection
    </div>
    <h1>Scan tires in seconds,<br>not hours.</h1>
    <p>Advanced computer vision system that identifies tire defects automatically — cracks, shelling, discoloration, and more.</p>
</div>
""", unsafe_allow_html=True)

# ==================== LOAD MODEL ====================
@st.cache_resource
def load_model():
    return YOLO('best.pt')

try:
    model = load_model()
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# ==================== TWO COLUMN LAYOUT ====================
col_left, col_right = st.columns([1, 1], gap="large")

# ==================== LEFT COLUMN - UPLOAD ====================
with col_left:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="upload-icon">📸</div>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; margin-bottom: 0.5rem;">Upload Tire Image</h3>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #71717A; font-size: 0.875rem; margin-bottom: 1.5rem;">JPG, PNG or JPEG — max 10MB</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    st.markdown('<div style="margin-top: 1rem;"><p style="color: #52525B; font-size: 0.7rem; text-align: center;">⬆️ Drag & drop or click to browse</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== RIGHT COLUMN - RESULT ====================
with col_right:
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        with st.spinner("Analyzing..."):
            time.sleep(0.3)
            results = model(tmp_path)
        
        result = results[0]
        
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-header">📊 Detection Result</div>', unsafe_allow_html=True)
        st.image(result.plot(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis section
        if result.boxes is not None and len(result.boxes) > 0:
            detected_classes = {}
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls]
                if class_name not in detected_classes:
                    detected_classes[class_name] = []
                detected_classes[class_name].append(conf)
            
            has_defect = any(c != "Wheel" for c in detected_classes.keys())
            
            st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
            
            # Metrics
            all_confs = []
            for confs in detected_classes.values():
                all_confs.extend(confs)
            max_conf = max(all_confs) if all_confs else 0.0
            
            st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-value">{max_conf:.1%}</div>
                    <div class="metric-label">Confidence</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">{'⚠️' if has_defect else '✅'}</div>
                    <div class="metric-label">Status</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">{len([c for c in detected_classes.keys() if c != 'Wheel'])}</div>
                    <div class="metric-label">Defects Found</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">{len(detected_classes)}</div>
                    <div class="metric-label">Total Objects</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detection details
            st.markdown('<p style="font-weight: 500; margin-bottom: 0.75rem;">🔍 Detected Items</p>', unsafe_allow_html=True)
            
            for class_name, confs in detected_classes.items():
                avg_conf = sum(confs) / len(confs)
                
                if class_name == "Wheel":
                    color = "#10B981"
                    border_color = "rgba(16, 185, 129, 0.2)"
                    badge = "🟢 Normal"
                elif class_name == "Cracks-Scratches":
                    color = "#F59E0B"
                    border_color = "rgba(245, 158, 11, 0.2)"
                    badge = "🟡 Crack / Scratch"
                elif class_name == "Shelling":
                    color = "#EF4444"
                    border_color = "rgba(239, 68, 68, 0.2)"
                    badge = "🔴 Shelling / Chunking"
                elif class_name == "Discoloration":
                    color = "#F59E0B"
                    border_color = "rgba(245, 158, 11, 0.2)"
                    badge = "🟡 Discoloration"
                else:
                    color = "#71717A"
                    border_color = "rgba(113, 113, 122, 0.2)"
                    badge = "⚪ Unknown"
                
                st.markdown(f"""
                <div class="detection-item" style="border-left-color: {color}; background: {border_color};">
                    <span><strong>{badge}</strong> {class_name}</span>
                    <span style="color: {color}; font-weight: 500;">{avg_conf:.1%}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendation
            if has_defect:
                st.markdown("""
                <div class="recommend-box">
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.25rem;">⚠️</span>
                        <span style="font-weight: 600;">Action Required</span>
                    </div>
                    <p style="color: #A1A1AA; font-size: 0.875rem; margin: 0;">Tire damage detected. Schedule an inspection at your nearest service center immediately.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="recommend-box">
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.25rem;">✅</span>
                        <span style="font-weight: 600;">All Good</span>
                    </div>
                    <p style="color: #A1A1AA; font-size: 0.875rem; margin: 0;">No defects detected. Your tire appears to be in healthy condition.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <span style="font-size: 3rem;">✅</span>
                <h3 style="margin-top: 0.5rem;">No Defects Detected</h3>
                <p style="color: #71717A;">The uploaded tire appears to be in good condition.</p>
            </div>
            """, unsafe_allow_html=True)
        
        os.unlink(tmp_path)
    
    else:
        st.markdown("""
        <div class="result-card">
            <div class="result-header">📊 Detection Result</div>
            <div style="padding: 3rem 2rem; text-align: center;">
                <div style="font-size: 3rem; opacity: 0.5;">🖼️</div>
                <h3 style="color: #A1A1AA; margin-top: 1rem;">No image uploaded</h3>
                <p style="color: #52525B; font-size: 0.875rem;">Upload a tire image to start detection</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== FEATURES SECTION ====================
st.markdown("""
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 3rem;">
    <div style="background: #18181B; border-radius: 20px; padding: 1.25rem; border: 1px solid #27272A;">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚡</div>
        <div style="font-weight: 600; margin-bottom: 0.25rem;">Real-time Detection</div>
        <div style="color: #71717A; font-size: 0.75rem;">Powered by YOLOv8</div>
    </div>
    <div style="background: #18181B; border-radius: 20px; padding: 1.25rem; border: 1px solid #27272A;">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
        <div style="font-weight: 600; margin-bottom: 0.25rem;">4 Defect Types</div>
        <div style="color: #71717A; font-size: 0.75rem;">Cracks, Shelling, Discoloration</div>
    </div>
    <div style="background: #18181B; border-radius: 20px; padding: 1.25rem; border: 1px solid #27272A;">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎯</div>
        <div style="font-weight: 600; margin-bottom: 0.25rem;">90% Accuracy</div>
        <div style="color: #71717A; font-size: 0.75rem;">Trained on 2,000+ images</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p>WheelScan — AI-powered tire defect detection system</p>
    <p style="margin-top: 0.5rem;">Dataset: Wheel Defect Detection (Roboflow) | Model: YOLOv8 | Project SC 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
