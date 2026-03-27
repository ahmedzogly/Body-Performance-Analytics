import streamlit as st
import pandas as pd
import joblib
import numpy as np

# إعداد واجهة التطبيق
st.set_page_config(page_title="نظام تقييم الأداء البدني الذكي", layout="wide")

st.title("🏋️ نظام تحليل وتصنيف الأداء البدني")
st.write("أدخل البيانات الحيوية للحصول على تقييم فوري لمستوى اللياقة البدنية.")

# تحميل النماذج
@st.cache_resource
def load_models():
    clf = joblib.load('classifier_model.pkl')
    reg = joblib.load('regression_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return clf, reg, scaler

clf, reg, scaler = load_models()

# تقسيم الواجهة إلى أعمدة لإدخال البيانات
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("العمر", min_value=10, max_value=100, value=25)
    gender = st.selectbox("الجنس", options=["ذكر", "أنثى"])
    height = st.number_input("الطول (سم)", min_value=100.0, max_value=250.0, value=170.0)

with col2:
    weight = st.number_input("الوزن (كجم)", min_value=30.0, max_value=200.0, value=70.0)
    body_fat = st.number_input("نسبة الدهون (%)", min_value=1.0, max_value=60.0, value=20.0)
    grip = st.number_input("قوة القبضة", min_value=0.0, max_value=100.0, value=40.0)

with col3:
    sit_bend = st.number_input("المرونة (سم)", min_value=-30.0, max_value=50.0, value=15.0)
    sit_ups = st.number_input("تمارين البطن (عدات)", min_value=0, max_value=100, value=40)
    diastolic = st.number_input("ضغط الدم الانبساطي", min_value=40.0, max_value=130.0, value=80.0)
    systolic = st.number_input("ضغط الدم الانقباضي", min_value=80.0, max_value=200.0, value=120.0)

# تحويل الجنس لرقم كما في مشروعك
gender_val = 0 if gender == "ذكر" else 1

# تجهيز البيانات للتنبؤ
input_data = pd.DataFrame([[age, gender_val, height, weight, body_fat, diastolic, systolic, grip, sit_bend, sit_ups]], 
                          columns=['age', 'gender', 'height_cm', 'weight_kg', 'body_fat_pct', 'diastolic', 'systolic', 'gripForce', 'sit_bend_forward_cm', 'sit_ups_counts'])

if st.button("تحليل الأداء البدني"):
    # 1. عمل Scaling للبيانات
    input_scaled = scaler.transform(input_data)
    
    # 2. التنبؤ بالفئة (Classification)
    prediction_class = clf.predict(input_scaled)[0]
    
    # 3. التنبؤ بمسافة القفز (Regression)
    prediction_jump = reg.predict(input_scaled)[0]
    
    # عرض النتائج
    st.divider()
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.metric(label="فئة الأداء المتوقعة", value=f"Grade {prediction_class}")
        st.info("A: ممتاز | B: جيد جداً | C: متوسط | D: ضعيف")
        
    with res_col2:
        st.metric(label="مسافة القفز الطويل المتوقعة", value=f"{prediction_jump:.2f} سم")