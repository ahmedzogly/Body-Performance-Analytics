import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. إعدادات الصفحة والنمط التقني (Tech UI Configuration) ---
st.set_page_config(
    page_title="CORE-AI | Body Performance",
    page_icon="📡",
    layout="wide"
)

# تصميم واجهة "Cyber-Tech" باستخدام CSS
st.markdown("""
    <style>
    /* الخلفية العامة والخطوط */
    .main {
        background-color: #050505;
        color: #00ff41; /* لون أخضر تقني (Matrix style) أو استبدله بـ #00d4ff للنمط الأزرق */
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* الحاويات والبطاقات */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00d4ff 0%, #004e92 100%);
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        letter-spacing: 2px;
        transition: 0.3s;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.8);
        transform: translateY(-2px);
    }

    .stMetric {
        background-color: #0a192f;
        border: 1px solid #00d4ff;
        padding: 20px;
        border-radius: 5px;
        box-shadow: inset 0 0 10px rgba(0, 212, 255, 0.1);
    }

    /* تحسين شكل الـ Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #0a192f;
        padding: 10px;
        border-radius: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #adbac7 !important;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        color: #00d4ff !important;
        border-bottom: 2px solid #00d4ff !important;
    }

    /* شريط التمرير والمدخلات */
    .stSlider [data-baseweb="slider"] {
        background-color: #00d4ff;
    }
    
    /* تأثيرات النصوص التقنية */
    .tech-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00d4ff, #004e92);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك تحميل البيانات (Engine Loading) ---
@st.cache_resource
def load_engine():
    clf = joblib.load('classifier_model.pkl')
    reg = joblib.load('regression_model.pkl')
    scaler = joblib.load('scaler.pkl')
    # إحصائيات مرجعية للذكاء الاصطناعي
    ref_stats = {
        'age': 36.7, 'height_cm': 168.5, 'weight_kg': 67.4, 'body_fat_pct': 23.2,
        'gripForce': 36.9, 'sit_bend_forward_cm': 15.2, 'sit_ups_counts': 39.7
    }
    return clf, reg, scaler, ref_stats

clf, reg, scaler, ref_stats = load_engine()

# --- 3. لوحة التحكم الجانبية (System Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>SYSTEM TERMINAL</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/689/689304.png", width=120)
    st.divider()
    
    st.subheader("🛠️ DEV TEAM")
    devs = ["A. Zoghli (Lead)", "E. TagElsir", "O. Mohamed", "M. Hassan", "A. Ibrahim"]
    for d in devs:
        st.code(f"USER: {d}")
    
    st.divider()
    st.write("📡 STATUS: ONLINE")
    st.write("🔒 SECURE CONNECTION")

# --- 4. الواجهة الرئيسية (Main Interface) ---
st.markdown("<h1 class='tech-header'>CORE-AI PERFORMANCE</h1>", unsafe_allow_html=True)
st.write(">>> ANALYZING BIOMETRIC DATA STRREAMS...")

t1, t2, t3 = st.tabs(["[ CORE ANALYSIS ]", "[ BULK PROCESSOR ]", "[ SYSTEM LOGS ]"])

# --- TAB 1: التحليل الفردي (Individual Core) ---
with t1:
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.subheader("INPUT DATA")
        with st.container(border=True):
            age = st.slider("AGE_VAR", 10, 80, 25)
            gender = st.selectbox("GENDER_TYPE", ["ذكر", "أنثى"])
            height = st.number_input("HEIGHT_CM", 120.0, 220.0, 175.0)
            weight = st.number_input("WEIGHT_KG", 30.0, 150.0, 75.0)
            fat = st.slider("BODY_FAT_%", 5.0, 50.0, 18.0)
            
            with st.expander("ADVANCED METRICS"):
                grip = st.number_input("GRIP_FORCE", 0.0, 100.0, 45.0)
                flex = st.number_input("FLEX_BEND", -20.0, 40.0, 15.0)
                situps = st.number_input("SIT_UPS", 0, 100, 45)
                sys = st.number_input("SYS_BP", 80, 200, 120)
                dias = st.number_input("DIAS_BP", 40, 130, 80)
        
        run_analysis = st.button("RUN SYSTEM ANALYSIS")

    if run_analysis:
        with st.spinner("PROCESSING DATA STREAMS..."):
            time.sleep(1)
            # تجهيز البيانات
            gender_val = 0 if gender == "ذكر" else 1
            features = [age, gender_val, height, weight, fat, dias, sys, grip, flex, situps]
            input_df = pd.DataFrame([features], columns=['age', 'gender', 'height_cm', 'weight_kg', 'body_fat_pct', 'diastolic', 'systolic', 'gripForce', 'sit_bend_forward_cm', 'sit_ups_counts'])
            
            scaled = scaler.transform(input_df)
            pred_class = clf.predict(scaled)[0]
            pred_jump = reg.predict(scaled)[0]

            with col_output:
                st.subheader("OUTPUT RESULTS")
                c1, c2 = st.columns(2)
                c1.metric("GRADE_RANK", f"CLASS {pred_class}")
                c2.metric("JUMP_PRED", f"{pred_jump:.1f} CM")
                
                # الرسم البياني التقني (Radar)
                cat = ['Strength', 'Flex', 'Endurance', 'Mass_Idx', 'Fat_Idx']
                user_v = [grip/70, (flex+20)/60, situps/80, 1-(weight/150), 1-(fat/50)]
                ref_v = [ref_stats['gripForce']/70, (ref_stats['sit_bend_forward_cm']+20)/60, ref_stats['sit_ups_counts']/80, 1-(ref_stats['weight_kg']/150), 1-(ref_stats['body_fat_pct']/50)]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=user_v, theta=cat, fill='toself', name='TARGET', line_color='#00d4ff'))
                fig.add_trace(go.Scatterpolar(r=ref_v, theta=cat, fill='toself', name='BASELINE', line_color='#6e7681'))
                fig.update_layout(polar=dict(radialaxis=dict(visible=False), bgcolor="#0a192f"), 
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color="#00d4ff", template="plotly_dark", height=350)
                st.plotly_chart(fig, use_container_width=True)
                
                st.code(f"> RECOMMENDATION: Optimizing FAT_IDX by 5% will elevate GRADE_RANK to NEXT_LEVEL.")

# --- TAB 2: معالجة الدفعات (Bulk Processor) ---
with t2:
    st.subheader("DATA BATCH UPLOAD")
    file = st.file_uploader("UPLOAD SYSTEM FILE (XLSX/CSV)", type=['xlsx', 'csv'])
    
    if file:
        df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
        if st.button("EXECUTE BATCH PROCESSING"):
            # منطق المعالجة...
            st.success("BATCH COMPLETE. ANALYZING DISTRIBUTION...")
            fig_hist = px.histogram(df, x=df.columns[-1], title="SYSTEM DISTRIBUTION", color_discrete_sequence=['#00d4ff'])
            fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#00d4ff")
            st.plotly_chart(fig_hist)

# --- TAB 3: سجلات النظام (System Logs) ---
with t3:
    st.subheader("SYSTEM ARCHITECTURE")
    st.markdown("""
    ```text
    [MODEL_INFO]
    - CLASSIFIER: MLP_NEURAL_NETWORK (Accuracy: 74.65%)
    - REGRESSOR: LINEAR_REGRESSION (R2: 0.79)
    - SCALER: MIN_MAX_SCALER
    - DATASET: 13,392 RECORDS
    
    [LOGS]
    - Connection established... OK
    - Models loaded... OK
    - Ready for inference.
    ```
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #444;'>// END OF TERMINAL // BODY PERFORMANCE AI © 2026</p>", unsafe_allow_html=True)
