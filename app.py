import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="Body Performance AI",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- إضافة لمسات CSS مخصصة ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #e94560;
        color: white;
        font-weight: bold;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- تحميل النماذج ---
@st.cache_resource
def load_models():
    clf = joblib.load('classifier_model.pkl')
    reg = joblib.load('regression_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return clf, reg, scaler

try:
    clf, reg, scaler = load_models()
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل النماذج: {e}")

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=100)
    st.title("لوحة التحكم")
    st.info("""
    **حول النظام:**
    هذا النظام يستخدم تقنيات الذكاء الاصطناعي (MLP) لتحليل الأداء البدني بناءً على بيانات أكثر من 13,000 رياضي.
    """)
    st.divider()
    st.write("🔧 **الإصدار:** 2.0.0")
    st.write("👤 *developers:👨‍💻 Team Members Ahmed Shehta Zoghli _ Eslam TagElsir _ Osama Mohamed _ Mohamed Hassan _ Ahmed Ibrahim")

# --- الواجهة الرئيسية ---
st.title("🏋️ نظام تحليل وتصنيف الأداء البدني الذكي")
st.write("قم بإدخال القياسات الحيوية للحصول على تحليل دقيق لمستوى اللياقة البدنية.")

# تقسيم الإدخال إلى تبويبات (Tabs) لتنظيم الواجهة
tab1, tab2 = st.tabs(["📝 إدخال البيانات", "📊 حول النماذج"])

with tab1:
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 المعلومات الأساسية")
            age = st.slider("العمر", 10, 80, 25)
            gender = st.radio("الجنس", ["ذكر", "أنثى"], horizontal=True)
            height = st.number_input("الطول (سم)", 100.0, 220.0, 175.0)
            weight = st.number_input("الوزن (كجم)", 30.0, 180.0, 75.0)
            body_fat = st.slider("نسبة الدهون (%)", 1.0, 50.0, 18.0)

        with col2:
            st.subheader("⚡ اختبارات الأداء")
            grip = st.number_input("قوة القبضة (Grip Force)", 0.0, 100.0, 45.0)
            sit_bend = st.number_input("المرونة (Sit & Bend - سم)", -20.0, 40.0, 15.0)
            sit_ups = st.number_input("تمارين البطن (Sit-ups)", 0, 100, 45)
            st.divider()
            st.subheader("🩸 الضغط")
            dias = st.number_input("الضغط الانبساطي (Diastolic)", 40, 120, 80)
            sys = st.number_input("الضغط الانقباضي (Systolic)", 80, 200, 120)

        submitted = st.form_submit_button("بدء التحليل الذكي")

    if submitted:
        with st.spinner('جاري تحليل البيانات ومقارنتها بالمعايير العالمية...'):
            time.sleep(1.5) # محاكاة وقت المعالجة
            
            # تجهيز البيانات
            gender_val = 0 if gender == "ذكر" else 1
            features = ['age', 'gender', 'height_cm', 'weight_kg', 'body_fat_pct', 
                        'diastolic', 'systolic', 'gripForce', 'sit_bend_forward_cm', 'sit_ups_counts']
            input_data = pd.DataFrame([[age, gender_val, height, weight, body_fat, dias, sys, grip, sit_bend, sit_ups]], 
                                      columns=features)
            
            # المعالجة والتنبؤ
            input_scaled = scaler.transform(input_data)
            pred_class = clf.predict(input_scaled)[0]
            pred_jump = reg.predict(input_scaled)[0]

            # عرض النتائج بشكل احترافي
            st.success("✅ تم اكتمال التحليل بنجاح!")
            
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                color = "green" if pred_class == 'A' else "orange" if pred_class in ['B', 'C'] else "red"
                st.markdown(f"""
                <div class="result-card">
                    <h3>فئة اللياقة</h3>
                    <h1 style='color:{color}; font-size: 80px;'>{pred_class}</h1>
                </div>
                """, unsafe_allow_html=True)

            with res_col2:
                st.markdown(f"""
                <div class="result-card">
                    <h3>مسافة القفز المتوقعة</h3>
                    <h1 style='color:#0f3460;'>{pred_jump:.1f} <span style='font-size: 20px;'>سم</span></h1>
                </div>
                """, unsafe_allow_html=True)

            with res_col3:
                # نصيحة بسيطة بناءً على النتائج
                if pred_class == 'A':
                    msg = "أداء ممتاز! استمر في المحافظة على هذا المستوى."
                elif pred_class == 'B':
                    msg = "مستوى جيد جداً، قليل من التركيز على المرونة سيجعلك في الفئة A."
                else:
                    msg = "تحتاج إلى خطة تدريبية مكثفة لتحسين قوة التحمل والمرونة."
                
                st.markdown(f"""
                <div class="result-card">
                    <h3>التوصية الذكية</h3>
                    <p style='font-size: 18px; padding-top: 20px;'>{msg}</p>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.subheader("تفاصيل النموذج الرياضي")
    st.write("""
    - **نموذج التصنيف:** Multi-Layer Perceptron (Neural Network) - دقة 74.6%
    - **نموذج الانحدار:** Linear Regression - R² Score 0.79
    - **البيانات:** تم التدريب على 13,392 عينة رياضية.
    """)
