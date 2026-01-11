import streamlit as st
import tensorflow as tf
import numpy as np
import os

# --- 1. SYSTEM CONFIGURATION (Full Screen & Dark) ---
st.set_page_config(
    page_title="CardioAI | Clinical Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. COMPLETE MEDICAL TERMINOLOGY MAPPING (ALL 50 CLASSES) ---
DIAGNOSIS_MAP = {
    '1AVB': 'First Degree AV Block',
    '2AVB': 'Second Degree AV Block',
    '3AVB': 'Third Degree AV Block',
    'AFIB': 'Atrial Fibrillation',
    'AFLT': 'Atrial Flutter',
    'ALMI': 'Anterolateral Myocardial Infarction',
    'AMI':  'Anterior Myocardial Infarction',
    'ASMI': 'Anteroseptal Myocardial Infarction',
    'CLBBB': 'Complete Left Bundle Branch Block',
    'CRBBB': 'Complete Right Bundle Branch Block',
    'DIG':  'Digoxin Effect',
    'EL':   'Electrolyte Disturbance',
    'ILBBB': 'Incomplete Left Bundle Branch Block',
    'ILMI': 'Inferolateral Myocardial Infarction',
    'IMI':  'Inferior Myocardial Infarction',
    'INJAL': 'Acute MI (Anterolateral)',
    'INJAS': 'Acute MI (Anteroseptal)',
    'INJIL': 'Acute MI (Inferolateral)',
    'INJIN': 'Acute MI (Inferior)',
    'INJLA': 'Acute MI (Lateral)',
    'IPLMI': 'Inferoposterolateral Myocardial Infarction',
    'IPMI': 'Inferoposterior Myocardial Infarction',
    'IRBBB': 'Incomplete Right Bundle Branch Block',
    'ISCAL': 'Ischemia (Anterolateral)',
    'ISCAN': 'Ischemia (Anterior)',
    'ISCAS': 'Ischemia (Anteroseptal)',
    'ISCIL': 'Ischemia (Inferolateral)',
    'ISCIN': 'Ischemia (Inferior)',
    'ISCLA': 'Ischemia (Lateral)',
    'ISC_':  'Non-Specific Ischemic Changes',
    'IVCD':  'Non-Specific Intraventricular Conduction Disturbance',
    'LAFB':  'Left Anterior Fascicular Block',
    'LAO/LAE': 'Left Atrial Enlargement',
    'LMI':   'Lateral Myocardial Infarction',
    'LNGQT': 'Long QT Syndrome',
    'LPFB':  'Left Posterior Fascicular Block',
    'LVH':   'Left Ventricular Hypertrophy',
    'NDT':   'Non-Diagnostic T-Wave Changes',
    'NORM':  'Normal Sinus Rhythm',
    'NST_':  'Non-Specific ST Changes',
    'PAC':   'Premature Atrial Contraction',
    'PACE':  'Paced Rhythm',
    'PMI':   'Posterior Myocardial Infarction',
    'PSVT':  'Paroxysmal Supraventricular Tachycardia',
    'PVC':   'Premature Ventricular Contraction',
    'RAO/RAE': 'Right Atrial Enlargement',
    'RVH':   'Right Ventricular Hypertrophy',
    'SEHYP': 'Septal Hypertrophy',
    'SR':    'Sinus Rhythm',
    'STACH': 'Sinus Tachycardia',
    'WPW':   'Wolff-Parkinson-White Syndrome'
}

CLASS_NAMES_RAW = [
    '1AVB', '2AVB', '3AVB', 'AFIB', 'AFLT', 'ALMI', 'AMI', 'ASMI', 'CLBBB', 'CRBBB', 
    'DIG', 'EL', 'ILBBB', 'ILMI', 'IMI', 'INJAL', 'INJAS', 'INJIL', 'INJIN', 'INJLA', 
    'IPLMI', 'IPMI', 'IRBBB', 'ISCAL', 'ISCAN', 'ISCAS', 'ISCIL', 'ISCIN', 'ISCLA', 
    'ISC_', 'IVCD', 'LAFB', 'LAO/LAE', 'LMI', 'LNGQT', 'LPFB', 'LVH', 'NDT', 'NORM', 
    'NST_', 'PAC', 'PACE', 'PMI', 'PSVT', 'PVC', 'RAO/RAE', 'RVH', 'SEHYP', 'SR', 
    'STACH', 'WPW'
]

# --- 3. ADVANCED CSS (Animations & Theme) ---
st.markdown("""
    <style>
    /* 1. FORCE DARK THEME & HIDE CLUTTER */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    header, footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* 2. BLINKING STATUS LIGHT */
    @keyframes blink {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #00FF88;
        border-radius: 50%;
        animation: blink 2s infinite;
        margin-right: 8px;
    }
    
    /* 3. CUSTOM PROGRESS BAR */
    .progress-container {
        width: 100%;
        background-color: #2b2b2b;
        border-radius: 4px;
        margin-top: 5px;
        height: 8px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease-in-out;
    }
    
    /* 4. DIAGNOSTIC PANELS */
    .metric-card {
        background-color: #1a1c24;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 8px;
    }
    .status-header {
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .diagnosis-text {
        font-size: 1.8rem;
        font-weight: 500;
        color: white;
    }
    
    /* 5. BUTTON STYLING */
    .stButton > button {
        background-color: #1F6FEB;
        color: white;
        border: none;
        padding: 12px;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton > button:hover { background-color: #1659C7; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE LOADER ---
@st.cache_resource
def load_engine():
    path = os.path.join(os.path.dirname(__file__), "final_heart_model.keras")
    if os.path.exists(path):
        return tf.keras.models.load_model(path)
    return None

model = load_engine()

# --- 5. TOP BAR (Status & Title) ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("## CardioAI <span style='color:#666; font-weight:300;'>| Clinical Diagnostic Suite</span>", unsafe_allow_html=True)
with col_head2:
    if model:
        st.markdown("<div style='text-align: right; padding-top: 10px;'><span class='status-indicator'></span><span style='color:#00FF88; font-weight:600; font-size:0.9rem;'>ENGINE ONLINE</span></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: right; color:#FF4B4B; font-weight:600;'>⚠ ENGINE OFFLINE</div>", unsafe_allow_html=True)

st.markdown("---")

# --- 6. MAIN WORKSPACE (Split Layout) ---
# Left: Controls | Right: Visualization & Results
left_panel, right_panel = st.columns([1, 2])

with left_panel:
    st.markdown("#### 1. Patient Data Import")
    uploaded_file = st.file_uploader("Upload 12-Lead Record (.npy)", type=["npy"])
    
    if uploaded_file and model:
        st.success("File Loaded Successfully")
        st.markdown("#### 2. Analysis Control")
        if st.button("RUN DIAGNOSTIC ALGORITHM", use_container_width=True):
            with st.spinner("Processing bio-signals..."):
                # Processing
                data = np.load(uploaded_file)
                if data.ndim == 2: data = np.expand_dims(data, axis=0)
                
                # Inference
                pred = model.predict(data)
                confidence = np.max(pred) * 100
                idx = np.argmax(pred)
                
                # Logic
                code = CLASS_NAMES_RAW[idx] if idx < len(CLASS_NAMES_RAW) else "UNK"
                full_name = DIAGNOSIS_MAP.get(code, f"Unspecified ({code})")
                
                # Store results in session state to persist on right panel
                st.session_state['result'] = {
                    'code': code,
                    'name': full_name,
                    'conf': confidence,
                    'data': data
                }

# --- 7. RIGHT PANEL (Results) ---
with right_panel:
    if 'result' in st.session_state and uploaded_file:
        res = st.session_state['result']
        
        # Determine Status Colors
        is_normal = res['code'] in ['NORM', 'SR']
        status_color = "#00FF88" if is_normal else "#FF4B4B" # Green vs Red
        status_text = "NORMAL SINUS RHYTHM" if is_normal else "ABNORMALITY DETECTED"
        
        # 1. Visualization
        st.markdown("#### Signal Trace (Lead I)")
        st.line_chart(res['data'][0,:,0], height=250)
        
        # 2. Diagnostic Card (FIXED INDENTATION)
        html_card = f"""
<div class="metric-card" style="border-left: 5px solid {status_color};">
    <div class="status-header" style="color: {status_color};">{status_text}</div>
    <div class="diagnosis-text">{res['name']}</div>
    <div style="margin-top: 15px; display: flex; justify-content: space-between; font-size: 0.9rem; color: #888;">
        <span>Classification Code: <b style="color: #ccc;">{res['code']}</b></span>
        <span>AI Confidence: <b style="color: #fff;">{res['conf']:.2f}%</b></span>
    </div>
    <div class="progress-container">
        <div class="progress-fill" style="width: {res['conf']}%; background-color: {status_color};"></div>
    </div>
</div>
"""
        st.markdown(html_card, unsafe_allow_html=True)
        
    elif uploaded_file:
        # Show Preview before analysis
        data_preview = np.load(uploaded_file)
        if data_preview.ndim == 2: data_preview = np.expand_dims(data_preview, axis=0)
        st.markdown("#### Signal Preview (Lead I)")
        st.line_chart(data_preview[0,:,0], height=250)
        st.info("← Click 'RUN DIAGNOSTIC ALGORITHM' to process this signal.")
    
    else:
        # Empty State
        st.markdown("""
        <div style="text-align: center; padding: 100px; color: #444; border: 2px dashed #333; border-radius: 10px;">
            <h3>Waiting for Data</h3>
            <p>Upload a patient file to begin analysis.</p>
        </div>
        """, unsafe_allow_html=True)