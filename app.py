import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objects as go
import time
from fpdf import FPDF
import base64

# --- 1. إعدادات النظام المتقدمة ---
st.set_page_config(
    page_title="TITAN-AI | Body Analytics",
    page_icon="⚡",
    layout="wide"
)

# تصميم الواجهة Tech Style (أحجام ضخمة وألوان نيون)
st.markdown("""
    <style>
    .main { background-color: #020617; color: #00f2ff; font-family: 'Segoe UI', sans-serif; }
    .tech-header {
        font-size: 4rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2ff, #0062ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 5px;
        text-align: center;
        text-shadow: 0 0 30px rgba(0, 242, 255, 0.3);
    }
    div[data-testid="stMetricValue"] { font-size: 75px !important; color: #00f2ff !important; }
    .stButton > button {
        width: 100% !important; height: 3.5em !important; font-size: 1.3rem !important;
        background: linear-gradient(45deg, #00f2ff, #0062ff) !important;
        border: none !important; color: white !important; font-weight: bold !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. وظيفة إنشاء تقرير PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'TITAN-AI: Body Performance Report', 0, 1, 'C')
        self.ln(10)

def create_pdf(name, age, gender, p_class, p_jump, recs):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Name: {name}", 0, 1)
    pdf.cell(0, 10, f"Age: {age} | Gender: {gender}", 0, 1)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"Final Performance Grade: {p_class}", 0, 1)
    pdf.cell(0, 10, f"Predicted Broad Jump: {p_jump:.2f} cm", 0, 1)
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 11)
    pdf.multi_cell(0, 10, f"System Recommendation: {recs}")
    return pdf.output(dest='S').encode('latin-1')

# --- 3. تحميل النماذج والبيانات ---
@st.cache_resource
def load_assets():
    clf = joblib.load('classifier_model.pkl')
    reg = joblib.load('regression_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return clf, reg, scaler

clf, reg, scaler = load_assets()

# --- 4. واجهة التطبيق ---
st.markdown("<h1 class='tech-header'>TITAN PERFORMANCE AI</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#00f2ff;'>📡 COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2097/2097276.png", width=120)
    st.divider()
    st.subheader("👥 DEV TEAM")
    for dev in ["A. Zoghli", "E. TagElsir", "O. Mohamed", "M. Hassan", "A. Ibrahim"]:
        st.code(f"ID: {dev.split('.')[1].strip().upper()}")

# الجزء الرئيسي للتحليل
col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.markdown("### 🧬 BIOMETRIC SCANNER")
    user_name = st.text_input("SUBJECT NAME", "Unknown Athlete")
    age = st.slider("AGE", 10, 80, 25)
    gender = st.selectbox("GENDER", ["ذكر", "أنثى"])
    height = st.number_input("HEIGHT (CM)", 120.0, 220.0, 175.0)
    weight = st.number_input("WEIGHT (KG)", 30.0, 150.0, 75.0)
    fat = st.slider("BODY FAT %", 5.0, 50.0, 18.0)
    
    with st.expander("⚡ ADVANCED PERFORMANCE DATA"):
        grip = st.number_input("GRIP STRENGTH", 0.0, 100.0, 45.0)
        flex = st.number_input("FLEXIBILITY (BEND)", -20.0, 40.0, 15.0)
        situps = st.number_input("CORE (SIT-UPS)", 0, 100, 45)
        sys = st.number_input("SYSTOLIC BP", 80, 200, 120)
        dias = st.number_input("DIASTOLIC BP", 40, 130, 80)

    analyze = st.button("RUN CORE SCAN")

if analyze:
    with st.spinner("PROCESSING DATA STREAMS..."):
        time.sleep(1)
        g_val = 0 if gender == "ذكر" else 1
        features = [age, g_val, height, weight, fat, dias, sys, grip, flex, situps]
        input_df = pd.DataFrame([features], columns=['age', 'gender', 'height_cm', 'weight_kg', 'body_fat_pct', 'diastolic', 'systolic', 'gripForce', 'sit_bend_forward_cm', 'sit_ups_counts'])
        
        scaled = scaler.transform(input_df)
        p_class = clf.predict(scaled)[0]
        p_jump = reg.predict(scaled)[0]

        with col_out:
            st.markdown("### 🛰️ ANALYTICAL OUTPUT")
            r1, r2 = st.columns(2)
            r1.metric("GRADE", f"RANK_{p_class}")
            r2.metric("POWER", f"{p_jump:.1f} CM")
            
            # توصية بسيطة للتقرير
            rec_text = f"The subject is classified as Grade {p_class}. Focus on flexibility and core stability is recommended to enhance explosive power."
            
            st.info(f"💡 {rec_text}")
            
            # زر تحميل التتقرير
            pdf_data = create_pdf(user_name, age, gender, p_class, p_jump, rec_text)
            st.download_button(
                label="📥 DOWNLOAD PERFORMANCE REPORT (PDF)",
                data=pdf_data,
                file_name=f"Report_{user_name}.pdf",
                mime="application/pdf"
            )
            
            # رسم بياني توضيحي
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = p_jump,
                title = {'text': "Explosive Power (Jump)"},
                gauge = {'axis': {'range': [None, 300]}, 'bar': {'color': "#00f2ff"}}
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#00f2ff", height=300)
            st.plotly_chart(fig, use_container_width=True)

st.markdown("<p style='text-align: center; color: #334155; margin-top: 50px;'>// TITAN CORE V4.0 // SECURE REPORTING ENABLED // 2026</p>", unsafe_allow_html=True)
