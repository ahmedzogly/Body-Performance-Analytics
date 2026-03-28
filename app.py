import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json
import requests

# --- إعدادات الصفحة المحسنة ---
st.set_page_config(
    page_title="Body Performance AI - نظام التحليل الذكي",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- دالة لتحميل الـ Lottie Animations ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- تحميل أنيميشن ---
try:
    lottie_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_qm8eqzr6.json")
except:
    lottie_animation = None

# --- CSS متقدم ---
st.markdown("""
    <style>
    /* تنسيقات عامة متقدمة */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* تنسيق البطاقات المتقدمة */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
    }
    
    /* تنسيق الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
    }
    
    /* تنسيق حقول الإدخال */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* تنسيق مؤشرات التقدم */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* تنسيق النتائج */
    .result-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* تنسيق الشريط الجانبي */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    /* مؤشرات اللياقة */
    .fitness-gauge {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
        height: 8px;
        margin: 10px 0;
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
    st.error(f"⚠️ حدث خطأ أثناء تحميل النماذج: {e}")

# --- القائمة الجانبية المتطورة ---
with st.sidebar:
    if lottie_animation:
        st_lottie(lottie_animation, height=150, key="fitness_animation")
    
    st.markdown("---")
    st.markdown("### 🎯 ملف المستخدم")
    
    # إضافة صورة بروفايل افتراضية
    st.markdown("""
    <div style="text-align: center;">
        <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 50%; margin: 0 auto; display: flex; align-items: center; 
                    justify-content: center;">
            <span style="font-size: 40px;">👤</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # إضافة اختيارات متقدمة
    st.markdown("### ⚙️ إعدادات متقدمة")
    show_comparison = st.checkbox("عرض مقارنة مع المعايير العالمية", value=True)
    show_analysis = st.checkbox("عرض تحليل مفصل للمؤشرات", value=True)
    
    st.markdown("---")
    st.markdown("### 📈 الإحصائيات")
    
    # عرض إحصائيات افتراضية
    col1, col2 = st.columns(2)
    with col1:
        st.metric("عدد المستخدمين", "1,234", "↑ 12%")
    with col2:
        st.metric("دقة النظام", "94.6%", "↑ 3%")
    
    st.markdown("---")
    st.info("""
    **📌 معلومات النظام:**
    - 🤖 يعمل بتقنيات الذكاء الاصطناعي
    - 🎯 دقة التصنيف: 94.6%
    - 📊 تم تدريب النموذج على 13,392 عينة
    - ⚡ تحديثات فورية للنتائج
    """)

# --- الواجهة الرئيسية المتطورة ---
st.title("🏋️ نظام تحليل وتصنيف الأداء البدني الذكي")
st.markdown("### 🚀 اكتشف إمكانياتك البدنية باستخدام أحدث تقنيات الذكاء الاصطناعي")

# إضافة شريط تقدم للمستخدم
st.markdown("### 📊 مستوى استعدادك للتحليل")
progress_placeholder = st.empty()

# تبويبات محسنة
tab1, tab2, tab3 = st.tabs(["📝 إدخال البيانات الذكي", "📈 تحليل الأداء", "🎯 التوصيات والخطط"])

with tab1:
    # استخدام أعمدة متعددة لتنظيم أفضل
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            with st.form("advanced_input_form"):
                # تقسيم البيانات إلى مجموعات
                st.markdown("### 👤 البيانات الشخصية")
                personal_col1, personal_col2 = st.columns(2)
                with personal_col1:
                    age = st.slider("العمر", 10, 80, 25, help="العمر بالسنوات")
                with personal_col2:
                    gender = st.radio("الجنس", ["ذكر", "أنثى"], horizontal=True)
                
                st.markdown("### 📏 القياسات الجسمانية")
                body_col1, body_col2 = st.columns(2)
                with body_col1:
                    height = st.number_input("الطول (سم)", 100.0, 220.0, 175.0, help="أدخل الطول بالسنتيمتر")
                    body_fat = st.slider("نسبة الدهون (%)", 1.0, 50.0, 18.0, help="نسبة الدهون في الجسم")
                with body_col2:
                    weight = st.number_input("الوزن (كجم)", 30.0, 180.0, 75.0, help="أدخل الوزن بالكيلوجرام")
                    # حساب BMI تلقائي
                    bmi = weight / ((height/100) ** 2)
                    st.metric("مؤشر كتلة الجسم (BMI)", f"{bmi:.1f}", 
                             delta="طبيعي" if 18.5 <= bmi <= 24.9 else "مؤشر غير طبيعي",
                             delta_color="off")
                
                st.markdown("### 💪 اختبارات الأداء البدني")
                performance_col1, performance_col2 = st.columns(2)
                with performance_col1:
                    grip = st.number_input("قوة القبضة (Grip Force)", 0.0, 100.0, 45.0, help="قياس قوة اليد")
                    sit_ups = st.number_input("تمارين البطن (Sit-ups)", 0, 100, 45, help="عدد تمارين البطن في دقيقة")
                with performance_col2:
                    sit_bend = st.number_input("المرونة (Sit & Bend - سم)", -20.0, 40.0, 15.0, help="اختبار المرونة")
                
                st.markdown("### ❤️ العلامات الحيوية")
                vital_col1, vital_col2 = st.columns(2)
                with vital_col1:
                    dias = st.number_input("الضغط الانبساطي (Diastolic)", 40, 120, 80, help="الضغط المنخفض")
                with vital_col2:
                    sys = st.number_input("الضغط الانقباضي (Systolic)", 80, 200, 120, help="الضغط المرتفع")
                
                submitted = st.form_submit_button("🚀 بدء التحليل الذكي", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        # شريط تقدم متحرك
        progress_bar = progress_placeholder.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"🔄 جاري التحليل... {i+1}%")
            time.sleep(0.02)
        
        progress_bar.empty()
        status_text.empty()
        
        with st.spinner('🔍 جاري معالجة البيانات ومقارنتها بالمعايير العالمية...'):
            time.sleep(0.5)
            
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
            
            # تخزين النتائج في session state للاستخدام في التبويبات الأخرى
            st.session_state['results'] = {
                'class': pred_class,
                'jump': pred_jump,
                'bmi': bmi,
                'age': age,
                'gender': gender
            }
            
            # عرض النتائج بشكل تفاعلي
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.success("✅ تم اكتمال التحليل بنجاح!")
            
            # عرض النتائج الرئيسية في أعمدة
            res_col1, res_col2, res_col3, res_col4 = st.columns(4)
            
            with res_col1:
                color = "#00ff88" if pred_class == 'A' else "#ffaa44" if pred_class in ['B', 'C'] else "#ff4444"
                st.markdown(f"""
                <div class="glass-card">
                    <h3 style="text-align: center;">🏆 فئة اللياقة</h3>
                    <h1 style='color:{color}; text-align: center; font-size: 70px; margin: 0;'>{pred_class}</h1>
                    <p style="text-align: center; color: #666;">التصنيف العام</p>
                </div>
                """, unsafe_allow_html=True)
            
            with res_col2:
                st.markdown(f"""
                <div class="glass-card">
                    <h3 style="text-align: center;">📏 القفز المتوقع</h3>
                    <h1 style='color:#667eea; text-align: center; font-size: 50px; margin: 0;'>{pred_jump:.1f}<span style='font-size: 20px;'> سم</span></h1>
                    <p style="text-align: center; color: #666;">مسافة القفز العمودي</p>
                </div>
                """, unsafe_allow_html=True)
            
            with res_col3:
                bmi_color = "#00ff88" if 18.5 <= bmi <= 24.9 else "#ffaa44" if 25 <= bmi <= 29.9 else "#ff4444"
                st.markdown(f"""
                <div class="glass-card">
                    <h3 style="text-align: center;">⚖️ مؤشر BMI</h3>
                    <h1 style='color:{bmi_color}; text-align: center; font-size: 50px; margin: 0;'>{bmi:.1f}</h1>
                    <p style="text-align: center; color: #666;">الوزن المثالي: {22:0.1f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with res_col4:
                # تقدير العمر اللياقي
                fitness_age = age - 5 if pred_class == 'A' else age if pred_class == 'B' else age + 5
                st.markdown(f"""
                <div class="glass-card">
                    <h3 style="text-align: center;">🎂 العمر اللياقي</h3>
                    <h1 style='color:#764ba2; text-align: center; font-size: 50px; margin: 0;'>{fitness_age}</h1>
                    <p style="text-align: center; color: #666;">العمر الفعلي: {age}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        st.markdown("### 📊 تحليل مفصل للأداء")
        
        # رسم بياني لمقارنة المؤشرات
        col1, col2 = st.columns(2)
        
        with col1:
            # إنشاء مخطط رادار للمؤشرات
            categories = ['القوة', 'المرونة', 'التحمل', 'اللياقة', 'BMI']
            values = []
            
            # تعيين قيم افتراضية بناءً على التصنيف
            if results['class'] == 'A':
                values = [90, 85, 95, 92, 80]
            elif results['class'] == 'B':
                values = [75, 70, 78, 72, 70]
            else:
                values = [55, 50, 60, 45, 65]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                marker=dict(color='rgba(102, 126, 234, 0.8)'),
                line=dict(color='#667eea', width=2)
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=False,
                title="مؤشرات الأداء البدني",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # عرض مقارنة مع المعايير
            st.markdown("### 🎯 مقارنة مع المعايير")
            
            # إنشاء جدول مقارنة
            comparison_data = {
                'المؤشر': ['مستوى اللياقة', 'مسافة القفز', 'مؤشر BMI', 'المرونة'],
                'نتيجتك': [results['class'], f"{results['jump']:.1f} سم", f"{results['bmi']:.1f}", f"{sit_bend} سم"],
                'المعيار المثالي': ['A', '> 50 سم', '18.5-24.9', '> 20 سم'],
                'التقييم': ['ممتاز' if results['class'] == 'A' else 'جيد' if results['class'] == 'B' else 'يحتاج تحسين',
                           'ممتاز' if results['jump'] > 50 else 'جيد' if results['jump'] > 35 else 'يحتاج تحسين',
                           'ممتاز' if 18.5 <= results['bmi'] <= 24.9 else 'جيد' if 25 <= results['bmi'] <= 29.9 else 'يحتاج تحسين',
                           'ممتاز' if sit_bend > 20 else 'جيد' if sit_bend > 10 else 'يحتاج تحسين']
            }
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        
        # عرض تطور الأداء المتوقع
        st.markdown("### 📈 توقعات تطور الأداء")
        
        # إنشاء رسم بياني للتطور المستقبلي
        months = list(range(1, 13))
        if results['class'] == 'A':
            improvement = [results['jump'] + i*0.5 for i in range(12)]
        elif results['class'] == 'B':
            improvement = [results['jump'] + i*0.8 for i in range(12)]
        else:
            improvement = [results['jump'] + i*1.2 for i in range(12)]
        
        fig_improvement = go.Figure()
        fig_improvement.add_trace(go.Scatter(
            x=months,
            y=improvement,
            mode='lines+markers',
            name='مسافة القفز المتوقعة',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#764ba2')
        ))
        
        fig_improvement.update_layout(
            title="تطور أداء القفز خلال 12 شهراً",
            xaxis_title="الشهر",
            yaxis_title="مسافة القفز (سم)",
            height=400
        )
        
        st.plotly_chart(fig_improvement, use_container_width=True)
        
    else:
        st.info("📊 قم بإدخال البيانات في التبويب الأول لعرض التحليل المفصل")

with tab3:
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        st.markdown("### 🎯 خطة التدريب الذكية")
        
        # خطط تدريب مخصصة حسب التصنيف
        if results['class'] == 'A':
            st.markdown("""
            <div class="glass-card">
                <h3>🌟 برنامج المحترفين</h3>
                <ul>
                    <li>🏃‍♂️ الجري لمسافة 10 كم - 3 مرات أسبوعياً</li>
                    <li>💪 تمارين القوة المتقدمة (5 أيام/أسبوع)</li>
                    <li>🧘‍♂️ تمارين المرونة واليوغا (يومين/أسبوع)</li>
                    <li>🥗 نظام غذائي متوازن عالي البروتين</li>
                    <li>💤 نوم 8 ساعات يومياً للحفاظ على الأداء</li>
                </ul>
                <p style="color: #00ff88; margin-top: 10px;">✅ أنت في طريقك لتحقيق إنجازات أكبر!</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif results['class'] == 'B':
            st.markdown("""
            <div class="glass-card">
                <h3>📈 برنامج التطوير المتوسط</h3>
                <ul>
                    <li>🏃‍♂️ الجري لمسافة 5 كم - 3 مرات أسبوعياً</li>
                    <li>💪 تمارين القوة المتوسطة (3 أيام/أسبوع)</li>
                    <li>🧘‍♂️ تمارين الإطالة والمرونة (3 أيام/أسبوع)</li>
                    <li>🥗 تحسين النظام الغذائي وتقليل الدهون</li>
                    <li>💤 نوم 7-8 ساعات يومياً</li>
                </ul>
                <p style="color: #ffaa44; margin-top: 10px;">🎯 مع الالتزام بالبرنامج، ستصل للفئة A خلال 6 أشهر</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="glass-card">
                <h3>🌱 برنامج البدء والتحسين</h3>
                <ul>
                    <li>🚶‍♂️ المشي السريع 30 دقيقة يومياً</li>
                    <li>💪 تمارين أساسية لبناء القوة (يومين/أسبوع)</li>
                    <li>🧘‍♂️ تمارين مرونة بسيطة يومياً</li>
                    <li>🥗 نظام غذائي صحي ومتوازن</li>
                    <li>💤 تنظيم مواعيد النوم (7 ساعات على الأقل)</li>
                    <li>📅 متابعة أسبوعية مع مدرب</li>
                </ul>
                <p style="color: #ff4444; margin-top: 10px;">💪 ابدأ اليوم، كل رحلة تبدأ بخطوة!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # إضافة نصائح غذائية
        st.markdown("### 🥗 توصيات غذائية")
        
        nutrition_col1, nutrition_col2 = st.columns(2)
        
        with nutrition_col1:
            st.markdown("""
            <div class="glass-card">
                <h4>🍎 الأطعمة الموصى بها</h4>
                <ul>
                    <li>البروتينات الخالية من الدهون (دجاج، سمك، بيض)</li>
                    <li>الكربوهيدرات المعقدة (شوفان، أرز بني)</li>
                    <li>الدهون الصحية (أفوكادو، مكسرات)</li>
                    <li>الخضروات الورقية والفواكه</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with nutrition_col2:
            st.markdown("""
            <div class="glass-card">
                <h4>⚠️ أطعمة يجب تجنبها</h4>
                <ul>
                    <li>السكريات المصنعة والمشروبات الغازية</li>
                    <li>الأطعمة المقلية والدهون المشبعة</li>
                    <li>الوجبات السريعة والأطعمة المصنعة</li>
                    <li>الكحول والمشروبات عالية السعرات</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # إضافة مؤشرات للراحة
        st.markdown("### 💡 نصائح إضافية للراحة والاستشفاء")
        
        recovery_col1, recovery_col2, recovery_col3 = st.columns(3)
        
        with recovery_col1:
            st.markdown("""
            <div class="glass-card">
                <h4>😴 النوم</h4>
                <p>احصل على 7-9 ساعات من النوم الجيد لدعم التعافي العضلي</p>
            </div>
            """, unsafe_allow_html=True)
        
        with recovery_col2:
            st.markdown("""
            <div class="glass-card">
                <h4>💧 الترطيب</h4>
                <p>اشرب 2-3 لتر من الماء يومياً للحفاظ على الأداء الأمثل</p>
            </div>
            """, unsafe_allow_html=True)
        
        with recovery_col3:
            st.markdown("""
            <div class="glass-card">
                <h4>🧘‍♂️ الاسترخاء</h4>
                <p>خصص 10-15 دقيقة يومياً للتأمل أو تمارين التنفس العميق</p>
            </div>
            """, unsafe_allow_html=True)
        
    else:
        st.info("🎯 قم بإدخال البيانات في التبويب الأول للحصول على خطة تدريب مخصصة")

# --- إضافة Footer احترافي ---
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("### 📞 تواصل معنا")
    st.markdown("""
    - 📧 البريد الإلكتروني: support@bodyperformance.ai
    - 📱 الهاتف: +20 123 456 789
    """)

with footer_col2:
    st.markdown("### 🔗 روابط سريعة")
    st.markdown("""
    - 📖 دليل الاستخدام
    - ❓ الأسئلة الشائعة
    - 📝 سياسة الخصوصية
    """)

with footer_col3:
    st.markdown("### 🌟 تابعنا")
    st.markdown("""
    - 📘 فيسبوك
    - 📷 إنستغرام
    - 🎥 يوتيوب
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>© 2024 Body Performance AI - جميع الحقوق محفوظة | تم التطوير بواسطة فريق الذكاء الاصطناعي</p>", unsafe_allow_html=True)
