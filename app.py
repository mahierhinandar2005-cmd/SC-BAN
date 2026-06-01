import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os
import time

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="WheelScan Pro - Deteksi Kerusakan Ban",
    page_icon="🛞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS (Bikin Keren) ====================
st.markdown("""
<style>
    /* Import font modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,100..900;1,100..900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header utama */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        border: 1px solid #334155;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .main-header p {
        color: #94A3B8;
        margin-top: 0.5rem;
        font-size: 1rem;
    }
    
    /* Card hasil deteksi */
    .result-card {
        background: #1E293B;
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid #334155;
        backdrop-filter: blur(10px);
    }
    
    .badge-success {
        background: #10B981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-danger {
        background: #EF4444;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-warning {
        background: #F59E0B;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #334155, transparent);
        margin: 2rem 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #0F172A 100%);
        border-right: 1px solid #334155;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #64748B;
        font-size: 0.75rem;
        border-top: 1px solid #334155;
        margin-top: 2rem;
    }
    
    /* Tombol upload */
    .upload-area {
        border: 2px dashed #334155;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        background: #0F172A;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #60A5FA;
        background: #1E293B;
    }
    
    /* Metrik card */
    .metric-card {
        background: #0F172A;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #334155;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #60A5FA;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 🛞 **WheelScan Pro**")
    st.markdown("---")
    
    st.markdown("#### 📋 **Tentang**")
    st.markdown("""
    Sistem deteksi kerusakan ban berbasis **YOLOv8** (CNN) yang dirancang untuk membantu teknisi dan pemilik kendaraan mendeteksi dini:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("✅ Retak (Cracks)")
        st.markdown("✅ Terkelupas (Shelling)")
    with col2:
        st.markdown("✅ Perubahan Warna")
        st.markdown("✅ Kondisi Normal")
    
    st.markdown("---")
    st.markdown("#### 🧠 **Teknologi**")
    st.markdown("""
    - **Model:** YOLOv8 (Ultralytics)
    - **Dataset:** 2.154+ gambar
    - **Akurasi mAP50:** 90%
    """)
    
    st.markdown("---")
    st.markdown("#### 📄 **Project**")
    st.markdown("SC 2026 | ANN-based Detection")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <p style="font-size: 0.7rem; color: #475569;">© 2026 · Built for Academic Project</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== HEADER UTAMA ====================
st.markdown("""
<div class="main-header">
    <h1>🛞 WheelScan Pro</h1>
    <p>Advanced Tire Defect Detection System — Scan. Detect. Act.</p>
</div>
""", unsafe_allow_html=True)

# ==================== LOAD MODEL ====================
@st.cache_resource
def load_model():
    with st.spinner("🔄 Memuat model kecerdasan buatan..."):
        model = YOLO('best.pt')
        return model

try:
    model = load_model()
    st.markdown("""
    <div style="background: #0F172A; border-radius: 12px; padding: 0.5rem 1rem; margin-bottom: 1rem; border-left: 3px solid #10B981;">
        <p style="color: #10B981; margin: 0;">✓ System ready · Model loaded successfully</p>
    </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.stop()

# ==================== UPLOAD AREA ====================
st.markdown("### 📸 Upload Gambar Ban")

uploaded_file = st.file_uploader(
    "Seret atau klik untuk memilih gambar",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

# Kolom untuk layout
col_left, col_right = st.columns([1, 1], gap="large")

# ==================== PROSES GAMBAR ====================
if uploaded_file is not None:
    # Simpan file sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    # Tampilkan gambar asli di kolom kiri
    with col_left:
        st.markdown("#### 📷 **Original Image**")
        original_image = Image.open(uploaded_file)
        st.image(original_image, use_container_width=True)
        st.caption(f"Resolusi: {original_image.size[0]} x {original_image.size[1]} px")
    
    # Deteksi
    with st.spinner("🔍 Menganalisis gambar..."):
        time.sleep(0.5)  # Efek loading
        results = model(tmp_path)
    
    result = results[0]
    
    # Tampilkan hasil deteksi di kolom kanan
    with col_right:
        st.markdown("#### 🎯 **Detection Result**")
        st.image(result.plot(), use_container_width=True)
    
    # ==================== HASIL ANALISIS ====================
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Hasil Analisis")
    
    if result.boxes is not None:
        # Hitung statistik
        detected_classes = {}
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = model.names[cls]
            if class_name not in detected_classes:
                detected_classes[class_name] = []
            detected_classes[class_name].append(conf)
        
        # Tampilkan metrik
        metric_cols = st.columns(4)
        
        # Total objek terdeteksi
        total_detections = sum(len(v) for v in detected_classes.values())
        with metric_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_detections}</div>
                <div class="metric-label">Total Deteksi</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Status keseluruhan
        has_defect = any(c != "Wheel" for c in detected_classes.keys())
        status_color = "#EF4444" if has_defect else "#10B981"
        status_text = "⚠️ RUSAK" if has_defect else "✅ SEHAT"
        with metric_cols[1]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {status_color};">{status_text}</div>
                <div class="metric-label">Status Ban</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Confidence rata-rata tertinggi
        max_conf = max(max(v) for v in detected_classes.values())
        with metric_cols[2]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{max_conf:.1%}</div>
                <div class="metric-label">Confidence Tertinggi</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Jumlah jenis kerusakan
        defect_types = [c for c in detected_classes.keys() if c != "Wheel"]
        with metric_cols[3]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(defect_types)}</div>
                <div class="metric-label">Jenis Kerusakan</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detail deteksi
        st.markdown("#### 🔍 **Detail Deteksi**")
        
        for class_name, confs in detected_classes.items():
            avg_conf = sum(confs) / len(confs)
            
            if class_name == "Wheel":
                st.markdown(f"""
                <div style="background: #0F172A; border-radius: 12px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-left: 3px solid #10B981;">
                    <span class="badge-success">NORMAL</span> <strong>{class_name}</strong>
                    <span style="float: right; color: #94A3B8;">confidence: {avg_conf:.1%}</span>
                </div>
                """, unsafe_allow_html=True)
            elif class_name == "Cracks-Scratches":
                st.markdown(f"""
                <div style="background: #0F172A; border-radius: 12px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-left: 3px solid #F59E0B;">
                    <span class="badge-warning">RETAK</span> <strong>{class_name}</strong>
                    <span style="float: right; color: #94A3B8;">confidence: {avg_conf:.1%}</span>
                </div>
                """, unsafe_allow_html=True)
            elif class_name == "Shelling":
                st.markdown(f"""
                <div style="background: #0F172A; border-radius: 12px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-left: 3px solid #EF4444;">
                    <span class="badge-danger">TERKELUPAS</span> <strong>{class_name}</strong>
                    <span style="float: right; color: #94A3B8;">confidence: {avg_conf:.1%}</span>
                </div>
                """, unsafe_allow_html=True)
            elif class_name == "Discoloration":
                st.markdown(f"""
                <div style="background: #0F172A; border-radius: 12px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-left: 3px solid #F59E0B;">
                    <span class="badge-warning">PERUBAHAN WARNA</span> <strong>{class_name}</strong>
                    <span style="float: right; color: #94A3B8;">confidence: {avg_conf:.1%}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Rekomendasi
        st.markdown("#### 💡 **Rekomendasi**")
        if has_defect:
            st.warning("""
            ⚠️ **Kerusakan terdeteksi pada ban Anda!**  
            Segera periksakan ke bengkel terdekat untuk penanganan lebih lanjut. Berkendara dengan ban rusak dapat membahayakan keselamatan.
            """)
        else:
            st.success("""
            ✅ **Ban dalam kondisi sehat!**  
            Teruskan perawatan rutin untuk menjaga performa ban tetap optimal.
            """)
    
    else:
        # Tidak ada deteksi
        st.markdown("""
        <div style="background: #0F172A; border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid #334155;">
            <h2 style="color: #10B981;">✅ Tidak Ada Kerusakan</h2>
            <p style="color: #94A3B8;">Model tidak mendeteksi adanya kerusakan pada ban. Kondisi ban terlihat normal.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 **Tips:** Pastikan gambar diambil dengan pencahayaan cukup dan ban terlihat jelas untuk hasil deteksi yang lebih akurat.")
    
    # Bersihkan file temporary
    os.unlink(tmp_path)

else:
    # Tampilan saat belum upload gambar
    with col_left:
        st.markdown("""
        <div class="upload-area">
            <h2 style="color: #60A5FA;">📤</h2>
            <h3 style="color: #F1F5F9;">Belum ada gambar</h3>
            <p style="color: #64748B;">Upload gambar ban untuk memulai deteksi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div style="background: #1E293B; border-radius: 20px; padding: 1.5rem;">
            <h4 style="color: #F1F5F9; margin-bottom: 1rem;">📌 Panduan</h4>
            <ul style="color: #94A3B8; line-height: 1.8;">
                <li>Gunakan gambar dengan pencahayaan yang cukup</li>
                <li>Pastikan ban terlihat jelas (tidak terlalu jauh)</li>
                <li>Format yang didukung: JPG, JPEG, PNG</li>
                <li>Hasil detiksi akan muncul dalam beberapa detik</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p>WheelScan Pro — Deteksi Kerusakan Ban dengan YOLOv8</p>
    <p style="font-size: 0.7rem;">Dataset: Wheel Defect Detection (Roboflow) | Project SC 2026</p>
</div>
""", unsafe_allow_html=True)
