import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os
import time

st.set_page_config(page_title="RailWheel Inspector", page_icon="🚆", layout="wide", initial_sidebar_state="collapsed")

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    .stApp { background: #0A0A0A; }
    
    .main-container { max-width: 1400px; margin: 0 auto; padding: 2rem; }
    
    /* Navbar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(10, 10, 10, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #2A2A2A;
        margin-bottom: 2rem;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-icon { font-size: 1.8rem; }
    
    .logo-text {
        font-size: 1.25rem;
        font-weight: 600;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Hero */
    .hero {
        text-align: center;
        padding: 2rem 2rem 3rem;
        background: linear-gradient(180deg, #0A0A0A 0%, #141414 100%);
        border-radius: 32px;
        margin-bottom: 3rem;
        border: 1px solid #2A2A2A;
    }
    
    .hero-badge {
        display: inline-block;
        background: #1A1A1A;
        border: 1px solid #3A3A3A;
        border-radius: 100px;
        padding: 0.25rem 1rem;
        font-size: 0.75rem;
        color: #FF8E53;
        margin-bottom: 1.5rem;
    }
    
    .hero h1 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .hero p { color: #A1A1AA; font-size: 1rem; max-width: 600px; margin: 0 auto; }
    
    /* Cards */
    .upload-card, .result-card {
        background: #141414;
        border-radius: 24px;
        border: 1px solid #2A2A2A;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .upload-card:hover { border-color: #4A4A4A; background: #1A1A1A; }
    
    .result-header {
        padding-bottom: 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #2A2A2A;
        font-weight: 600;
        color: #FFFFFF;
    }
    
    /* Metric Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-item {
        background: #1A1A1A;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #2A2A2A;
    }
    
    .metric-value { font-size: 1.75rem; font-weight: 700; color: #FFFFFF; }
    .metric-label { font-size: 0.75rem; color: #71717A; margin-top: 0.25rem; }
    
    /* Detection Item */
    .detection-item {
        background: #1A1A1A;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid;
    }
    
    /* Recommendation */
    .recommend-box {
        background: #1A1A1A;
        border-radius: 16px;
        padding: 1.25rem;
        margin-top: 1rem;
        border: 1px solid #2A2A2A;
    }
    
    /* Features */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-top: 3rem;
    }
    
    .feature-card {
        background: #141414;
        border-radius: 20px;
        padding: 1.25rem;
        border: 1px solid #2A2A2A;
        text-align: center;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #52525B;
        font-size: 0.75rem;
        border-top: 1px solid #2A2A2A;
        margin-top: 3rem;
    }
    
    button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
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
        <span class="logo-icon">🚆</span>
        <span class="logo-text">RailWheel Inspector</span>
    </div>
    <div style="color: #71717A; font-size: 0.875rem;">Industrial AI for Railway Maintenance</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ==================== HERO ====================
st.markdown("""
<div class="hero">
    <div class="hero-badge">
        🚆 AI-Powered Railway Wheel Inspection
    </div>
    <h1>Detect wheel defects<br>before they become failures.</h1>
    <p>Computer vision system for automatic detection of cracks, shelling, and discoloration on railway wheels — enabling predictive maintenance.</p>
</div>
""", unsafe_allow_html=True)

# ==================== LOAD MODEL ====================
@st.cache_resource
def load_model():
    return YOLO('best.pt')

try:
    model = load_model()
    st.markdown("""
    <div style="background: #141414; border-radius: 12px; padding: 0.5rem 1rem; margin-bottom: 1rem; border-left: 3px solid #10B981;">
        <p style="color: #10B981; margin: 0; font-size: 0.875rem;">✓ System ready · Model loaded</p>
    </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# ==================== TWO COLUMN ====================
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="upload-icon" style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">📷</div>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; margin-bottom: 0.5rem;">Upload Wheel Image</h3>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #71717A; font-size: 0.875rem; margin-bottom: 1.5rem;">JPG, PNG — max 10MB</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    st.markdown('<p style="color: #52525B; font-size: 0.7rem; text-align: center; margin-top: 1rem;">⬆️ Drag & drop or click to browse</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        with st.spinner("Analyzing wheel image..."):
            time.sleep(0.3)
            results = model(tmp_path)
        
        result = results[0]
        
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-header">🔍 Inspection Result</div>', unsafe_allow_html=True)
        st.image(result.plot(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
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
                    <div class="metric-label">Objects</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<p style="font-weight: 500; margin-bottom: 0.75rem;">📋 Defect Details</p>', unsafe_allow_html=True)
            
            for class_name, confs in detected_classes.items():
                avg_conf = sum(confs) / len(confs)
                
                if class_name == "Wheel":
                    color = "#10B981"
                    badge = "🟢 Normal"
                elif class_name == "Cracks-Scratches":
                    color = "#F59E0B"
                    badge = "🟡 Crack Detected"
                elif class_name == "Shelling":
                    color = "#EF4444"
                    badge = "🔴 Shelling Detected"
                elif class_name == "Discoloration":
                    color = "#F59E0B"
                    badge = "🟡 Discoloration"
                else:
                    color = "#71717A"
                    badge = "⚪ Unknown"
                
                st.markdown(f"""
                <div class="detection-item" style="border-left-color: {color};">
                    <span><strong>{badge}</strong> {class_name}</span>
                    <span style="color: {color};">{avg_conf:.1%}</span>
                </div>
                """, unsafe_allow_html=True)
            
            if has_defect:
                st.markdown("""
                <div class="recommend-box">
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.25rem;">⚠️</span>
                        <span style="font-weight: 600;">Maintenance Required</span>
                    </div>
                    <p style="color: #A1A1AA; font-size: 0.875rem; margin: 0;">Wheel defect detected. Schedule inspection and maintenance before next operation.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="recommend-box">
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.25rem;">✅</span>
                        <span style="font-weight: 600;">Wheel is Healthy</span>
                    </div>
                    <p style="color: #A1A1AA; font-size: 0.875rem; margin: 0;">No defects detected. Continue routine maintenance schedule.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <span style="font-size: 3rem;">✅</span>
                <h3 style="margin-top: 0.5rem;">No Defects Detected</h3>
                <p style="color: #71717A;">The wheel appears to be in good condition.</p>
            </div>
            """, unsafe_allow_html=True)
        
        os.unlink(tmp_path)
    
    else:
        st.markdown("""
        <div class="result-card">
            <div class="result-header">🔍 Inspection Result</div>
            <div style="padding: 3rem 2rem; text-align: center;">
                <div style="font-size: 3rem; opacity: 0.5;">🚆</div>
                <h3 style="color: #A1A1AA; margin-top: 1rem;">No image uploaded</h3>
                <p style="color: #52525B; font-size: 0.875rem;">Upload a railway wheel image to start inspection</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== FEATURES ====================
st.markdown("""
<div class="features-grid">
    <div class="feature-card">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🛤️</div>
        <div style="font-weight: 600;">Railway Infrastructure</div>
        <div style="color: #71717A; font-size: 0.75rem;">Industrial-grade inspection system</div>
    </div>
    <div class="feature-card">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔍</div>
        <div style="font-weight: 600;">3 Defect Types</div>
        <div style="color: #71717A; font-size: 0.75rem;">Cracks, Shelling, Discoloration</div>
    </div>
    <div class="feature-card">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
        <div style="font-weight: 600;">90% Accuracy</div>
        <div style="color: #71717A; font-size: 0.75rem;">Trained on railway wheel dataset</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p>RailWheel Inspector — AI-powered railway wheel defect detection for predictive maintenance</p>
    <p style="margin-top: 0.5rem;">Dataset: Wheel Defect Detection (Railway) | Model: YOLOv8 | Project SC 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
