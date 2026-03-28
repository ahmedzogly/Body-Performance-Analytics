import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="Body Performance AI Pro",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إضافة CSS مخصص لتحسين المظهر وجعله يبدو كمنصة تحليلية
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: #161b22;
        border-radius: 10px 10px 0px 0px; color: #adbac7;
    }
    .stTabs [aria-selected="true"] { background-color: #e94560 !important; color: white !important; }
    div[data-testid="stMetricValue"] { font-size: 40px; color: #e94560; }
    .footer-text { text-align: center; color: #6e7681; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. تحميل النماذج والبيانات المرجعية ---
@st.cache_resource
def load_assets():
    clf = joblib.load('classifier_model.pkl')
    reg = joblib.load('regression_model.pkl')
    scaler = joblib.load('scaler.pkl')
    # بيانات مرجعية للمقارنة (المتوسطات العامة من قاعدة البيانات)
    reference_stats = {
        'age': 36.7, 'height_cm': 168.5, 'weight_kg': 67.4, 'body_fat_pct': 23.2,
        'gripForce': 36.9, 'sit_bend_forward_cm': 15.2, 'sit_ups_counts': 39.7, 'broad_jump_cm': 190.1
    }
    return clf, reg, scaler, reference_stats

try:
    clf, reg, scaler, ref_stats = load_assets()
except Exception as e:
    st.error(f"Error loading models: {e}")

# --- 3. القائمة الجانبية (فريق العمل) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8360/8360914.png", width=100)
    st.title("Body Performance AI")
    st.markdown("---")
    st.subheader("👥 فريق التطوير")
    st.markdown("""
    - **أحمد شحتة** (Team Lead)
    - **إسلام تاجي**
    - **أسامة محمد**
    - **محمد حسن**
    - **أحمد إبراهيم**
    """)
    st.markdown("---")
    st.info("نظام ذكي يعتمد على MLP و Linear Regression لتحليل الكفاءة البدنية.")

# --- 4. الواجهة الرئيسية الرئيسية ---
st.title("🏋️ منصة التحليل الذكي للأداء البدني")
st.markdown("مرحباً بك! اختر نوع التحليل المطلوب من التبويبات أدناه:")

tab1, tab2, tab3 = st.tabs(["🎯 تحليل فردي & سيناريوهات", "📁 تحليل ملفات Excel/CSV", "📈 منهجية العمل"])

# --- TAB 1: التحليل الفردي و What-If Analysis ---
with tab1:
    col_input, col_viz = st.columns([1, 1.5])
    
    with col_input:
        st.subheader("📝 إدخال البيانات")
        with st.expander("👤 البيانات الأساسية", expanded=True):
            age = st.slider("العمر", 10, 80, 25)
            gender = st.radio("الجنس", ["ذكر", "أنثى"], horizontal=True)
            height = st.number_input("الطول (سم)", 120.0, 220.0, 175.0)
            weight = st.number_input("الوزن (كجم)", 30.0, 150.0, 75.0)
            fat = st.slider("نسبة الدهون (%)", 5.0, 50.0, 18.0)

        with st.expander("⚡ اختبارات الأداء", expanded=True):
            grip = st.number_input("قوة القبضة", 0.0, 100.0, 45.0)
            flex = st.number_input("المرونة (Sit & Bend)", -20.0, 40.0, 15.0)
            situps = st.number_input("تمارين البطن (Sit-ups)", 0, 100, 45)
            sys = st.number_input("الضغط الانقباضي", 80, 200, 120)
            dias = st.number_input("الضغط الانبساطي", 40, 130, 80)

    with col_viz:
        st.subheader("📊 نتائج التحليل والمقارنة")
        
        # معالجة البيانات
        gender_val = 0 if gender == "ذكر" else 1
        features = [age, gender_val, height, weight, fat, dias, sys, grip, flex, situps]
        input_df = pd.DataFrame([features], columns=['age', 'gender', 'height_cm', 'weight_kg', 'body_fat_pct', 'diastolic', 'systolic', 'gripForce', 'sit_bend_forward_cm', 'sit_ups_counts'])
        
        # التنبؤ
        scaled_data = scaler.transform(input_df)
        pred_class = clf.predict(scaled_data)[0]
        pred_jump = reg.predict(scaled_data)[0]

        # عرض المقاييس
        m1, m2 = st.columns(2)
        m1.metric("التصنيف المتوقع", f"الفئة {pred_class}")
        m2.metric("قوة القفز (توقع)", f"{pred_jump:.1f} سم")

        # رسم بياني راداري (Radar Chart) للمقارنة
        categories = ['القوة', 'المرونة', 'التحمل', 'كتلة الجسم (عكسي)', 'الدهون (عكسي)']
        # قيم معالجة للعرض (Scaling for visualization)
        user_vals = [grip/70, (flex+20)/60, situps/80, 1-(weight/150), 1-(fat/50)]
        ref_vals = [ref_stats['gripForce']/70, (ref_stats['sit_bend_forward_cm']+20)/60, ref_stats['sit_ups_counts']/80, 1-(ref_stats['weight_kg']/150), 1-(ref_stats['body_fat_pct']/50)]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=user_vals, theta=categories, fill='toself', name='أداؤك', line_color='#e94560'))
        fig.add_trace(go.Scatterpolar(r=ref_vals, theta=categories, fill='toself', name='المعدل العام', line_color='#adbac7'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=False)), showlegend=True, template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)

        st.info(f"💡 **تحليل السيناريو:** لو قمت بتقليل نسبة الدهون إلى {max(5.0, fat-5):.1f}%، قد يتحسن أداؤك بنسبة ملحوظة!")

# --- TAB 2: تحليل الملفات (Bulk Processing) ---
with tab2:
    st.subheader("📁 تحليل المجموعات (Batch Processing)")
    st.write("ارفع ملف Excel أو CSV يحتوي على بيانات المتدربين (تأكد من مطابقة أسماء الأعمدة).")
    
    up_file = st.file_uploader("اختر الملف", type=['xlsx', 'csv'])
    
    if up_file:
        batch_df = pd.read_excel(up_file) if up_file.name.endswith('.xlsx') else pd.read_csv(up_file)
        
        if st.button("بدء المعالجة الذكية"):
            with st.spinner("جاري تحليل قاعدة البيانات..."):
                try:
                    # تحويل الجنس إذا كان نصياً
                    if 'gender' in batch_df.columns and batch_df['gender'].dtype == object:
                        batch_df['gender'] = batch_df['gender'].map({'M': 0, 'F': 1, 'ذكر': 0, 'أنثى': 1, 'male': 0, 'female': 1})
                    
                    cols = ['age', 'gender', 'height_cm', 'weight_kg', 'body_fat_pct', 'diastolic', 'systolic', 'gripForce', 'sit_bend_forward_cm', 'sit_ups_counts']
                    X_batch = batch_df[cols]
                    X_batch_scaled = scaler.transform(X_batch)
                    
                    batch_df['Predicted_Class'] = clf.predict(X_batch_scaled)
                    batch_df['Predicted_Jump'] = reg.predict(X_batch_scaled)
                    
                    st.success(f"تمت معالجة {len(batch_df)} سجل بنجاح!")
                    
                    # عرض توزيع النتائج
                    fig_dist = px.histogram(batch_df, x="Predicted_Class", color="Predicted_Class", 
                                            title="توزيع فئات اللياقة في المجموعة", color_discrete_sequence=px.colors.qualitative.Pastel)
                    st.plotly_chart(fig_dist)
                    
                    st.dataframe(batch_df.head(20))
                    
                    # تحميل النتائج
                    output_csv = batch_df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("تحميل النتائج كاملة", output_csv, "body_performance_results.csv", "text/csv")
                except Exception as e:
                    st.error(f"حدث خطأ في معالجة الملف: {e}. يرجى التأكد من تطابق الأعمدة مع النموذج.")

# --- TAB 3: منهجية العمل والتقنيات ---
with tab3:
    st.subheader("🔬 المنهجية العلمية والتقنية")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        **1. معالجة البيانات (Pre-processing):**
        - تنظيف 13,392 سجلاً من التناقضات.
        - استخدام `MinMaxScaler` لتوحيد أوزان الميزات.
        
        **2. النماذج المستخدمة:**
        - **التصنيف:** الشبكات العصبية (MLP) بدقة **74.65%**.
        - **الانحدار:** الانحدار الخطي (Linear Regression) بمعامل ارتباط **0.79**.
        """)
    with c2:
        st.markdown("""
        **3. أهم الميزات (Feature Importance):**
        أظهرت النتائج أن **المرونة (Sit & Bend)** و**نسبة الدهون** هما الأثر الأكبر في تحديد الفئة الرياضية.
        
        **4. البيئة التقنية:**
        - Python / Scikit-Learn / Streamlit / Plotly.
        """)

st.markdown("---")
st.markdown('<p class="footer-text">Introduction to AI and ML | March 2026 | Developed by Team Zoghli & Co.</p>', unsafe_allow_html=True)
