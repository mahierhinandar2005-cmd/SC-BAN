# ==================== PROSES HASIL DETEKSI DENGAN FILTER ====================
if result.boxes is not None and len(result.boxes) > 0:
    detected_classes = {}
    
    # Filter deteksi dengan confidence > 0.5 dan gabung yang sama
    for box in result.boxes:
        conf = float(box.conf[0])
        
        # SKIP kalo confidence kurang dari 50% (biar gak numpuk deteksi gak jelas)
        if conf < 0.5:
            continue
            
        cls = int(box.cls[0])
        class_name = model.names[cls]
        
        if class_name not in detected_classes:
            detected_classes[class_name] = []
        detected_classes[class_name].append(conf)
    
    # Kalo setelah filter jadi kosong, anggap gak ada deteksi
    if not detected_classes:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <span style="font-size: 3rem;">✅</span>
            <h3 style="margin-top: 0.5rem;">No Significant Defects</h3>
            <p style="color: #71717A;">Minor detections below threshold ignored.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        has_defect = any(c != "Wheel" for c in detected_classes.keys())
        
        # Ambil confidence tertinggi per kelas (bukan semua)
        best_confs = {}
        for class_name, confs in detected_classes.items():
            best_confs[class_name] = max(confs)
        
        all_confs = list(best_confs.values())
        max_conf = max(all_confs) if all_confs else 0.0
        
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value">{max_conf:.1%}</div>
                <div class="metric-label">Peak Confidence</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{'⚠️' if has_defect else '✅'}</div>
                <div class="metric-label">Status</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{len([c for c in best_confs.keys() if c != 'Wheel'])}</div>
                <div class="metric-label">Defect Types</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{len(best_confs)}</div>
                <div class="metric-label">Detected Objects</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p style="font-weight: 500; margin-bottom: 0.75rem;">📋 Defect Details</p>', unsafe_allow_html=True)
        
        # Tampilkan per KELAS (bukan per detection)
        for class_name, best_conf in best_confs.items():
            if class_name == "Wheel":
                color = "#10B981"
                badge = "🟢 Normal"
                border_color = "rgba(16, 185, 129, 0.15)"
            elif class_name == "Cracks-Scratches":
                color = "#F59E0B"
                badge = "🟡 Crack Detected"
                border_color = "rgba(245, 158, 11, 0.15)"
            elif class_name == "Shelling":
                color = "#EF4444"
                badge = "🔴 Shelling Detected"
                border_color = "rgba(239, 68, 68, 0.15)"
            elif class_name == "Discoloration":
                color = "#F59E0B"
                badge = "🟡 Discoloration"
                border_color = "rgba(245, 158, 11, 0.15)"
            else:
                color = "#71717A"
                badge = "⚪ Unknown"
                border_color = "rgba(113, 113, 122, 0.15)"
            
            st.markdown(f"""
            <div class="detection-item" style="border-left-color: {color}; background: {border_color};">
                <span><strong>{badge}</strong> {class_name}</span>
                <span style="color: {color}; font-weight: 600;">{best_conf:.1%}</span>
            </div>
            """, unsafe_allow_html=True)
