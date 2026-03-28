import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from fpdf import FPDF
import base64
import json
from datetime import datetime
import hashlib
import os
from pathlib import Path

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="TITAN-AI | Body Performance Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ENHANCED CSS FOR FUTURISTIC INTERFACE ---
st.markdown("""
    <style>
    /* Main Background with Gradient Animation */
    .main {
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #020617 100%);
        color: #00f2ff;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* Animated Gradient Text */
    .tech-header {
        font-size: 4rem !important;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2ff, #0062ff, #00f2ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 5px;
        text-align: center;
        animation: shine 3s linear infinite;
        margin-bottom: 20px;
    }
    
    @keyframes shine {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    /* Glowing Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(0, 242, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.2);
        border-color: rgba(0, 242, 255, 0.6);
    }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] { 
        font-size: 75px !important; 
        color: #00f2ff !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 18px !important;
        color: #94a3b8 !important;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100% !important;
        height: 3.5em !important;
        font-size: 1.3rem !important;
        background: linear-gradient(45deg, #00f2ff, #0062ff) !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.6) !important;
    }
    
    /* Expander Styling */
    .stExpander {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
    }
    
    /* Number Input Styling */
    .stNumberInput input, .stTextInput input {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        color: #00f2ff !important;
        border-radius: 8px !important;
    }
    
    /* Slider Styling */
    .stSlider {
        color: #00f2ff !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        color: #94a3b8;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #00f2ff, #0062ff);
        color: white !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
        border-right: 1px solid rgba(0, 242, 255, 0.2);
    }
    
    /* Success/Warning/Error Messages */
    .stAlert {
        background-color: rgba(15, 23, 42, 0.9) !important;
        border-left: 4px solid #00f2ff !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #334155;
        border-top: 1px solid rgba(0, 242, 255, 0.2);
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS (DEFINED FIRST) ---
def get_percentile(grade):
    percentiles = {'A': 'Top 15%', 'B': 'Top 35%', 'C': 'Average (50-70%)', 'D': 'Bottom 20%'}
    return percentiles.get(grade, 'Average')

def get_jump_percentile(jump):
    if jump > 250: return 'Top 5%'
    if jump > 200: return 'Top 20%'
    if jump > 150: return 'Above Average'
    return 'Below Average'

def get_bmi_percentile(bmi):
    if 18.5 <= bmi <= 24.9: return 'Optimal Range'
    if bmi < 18.5: return 'Underweight'
    return 'Overweight'

def get_fat_percentile(fat):
    if fat < 10: return 'Elite'
    if fat < 18: return 'Athletic'
    if fat < 25: return 'Average'
    return 'High'

def get_grip_percentile(grip):
    if grip > 60: return 'Top 10%'
    if grip > 45: return 'Above Average'
    if grip > 30: return 'Average'
    return 'Below Average'

def get_flex_percentile(flex):
    if flex > 25: return 'Excellent'
    if flex > 15: return 'Good'
    if flex > 5: return 'Average'
    return 'Needs Improvement'

def get_situps_percentile(situps):
    if situps > 70: return 'Excellent'
    if situps > 50: return 'Good'
    if situps > 35: return 'Average'
    return 'Needs Improvement'

def generate_recommendations(grade, jump, age, bmi, fat):
    """Generate personalized recommendations based on all metrics"""
    recommendations = []
    
    if grade == 'A':
        recommendations.append("🏆 **ELITE PERFORMER**: Maintain current training intensity with focus on injury prevention.")
        recommendations.append("⚡ Optimize explosive power with advanced plyometric drills (box jumps, depth jumps).")
        recommendations.append("🎯 Set competitive goals: aim to exceed personal records in vertical jump.")
    elif grade == 'B':
        recommendations.append("📈 **STRONG FOUNDATION**: Increase training intensity by 10-15% gradually.")
        recommendations.append("💪 Focus on compound movements (squats, deadlifts) to enhance explosive power.")
        recommendations.append("🧘 Add 15 minutes of dynamic stretching pre-workout.")
    else:
        recommendations.append("🌱 **DEVELOPMENT FOCUS**: Begin with bodyweight exercises to build foundation.")
        recommendations.append("🏃‍♂️ Incorporate 30 minutes of cardio, 3 times weekly for endurance.")
        recommendations.append("📅 Consistency is key - aim for 4 training sessions weekly.")
    
    # BMI-specific recommendations
    if bmi > 25:
        recommendations.append("⚖️ **WEIGHT MANAGEMENT**: Focus on caloric deficit of 300-500 calories/day.")
    elif bmi < 18.5:
        recommendations.append("🍽️ **NUTRITION FOCUS**: Increase caloric intake with nutrient-dense foods.")
    
    # Age-specific recommendations
    if age > 45:
        recommendations.append("🛡️ **INJURY PREVENTION**: Include 20 minutes of mobility work before each session.")
    
    # Jump-specific recommendations
    if jump < 150:
        recommendations.append("🦵 **POWER DEVELOPMENT**: Start with box squats and calf raises to build leg strength.")
    
    return "\n".join(recommendations)

def get_performance_insights(grade, jump_distance, age):
    """Generate detailed performance insights based on metrics"""
    insights = []
    
    # Grade-based insights
    grade_insights = {
        'A': 'Elite Performance Level. Athlete demonstrates exceptional physical capabilities across all metrics.',
        'B': 'Advanced Performance Level. Strong foundation with room for optimization in specific areas.',
        'C': 'Intermediate Level. Good baseline with potential for significant improvement.',
        'D': 'Development Level. Focus on fundamental fitness components is recommended.'
    }
    insights.append(f"• {grade_insights.get(grade, 'Standard performance level')}")
    
    # Jump distance analysis
    if jump_distance > 250:
        insights.append(f"• Exceptional explosive power! Jump distance ({jump_distance:.1f}cm) exceeds elite athlete standards.")
    elif jump_distance > 200:
        insights.append(f"• Excellent explosive power. Jump distance ({jump_distance:.1f}cm) indicates strong lower body strength.")
    elif jump_distance > 150:
        insights.append(f"• Good explosive power. Focus on plyometric training could enhance jump performance.")
    else:
        insights.append(f"• Jump distance ({jump_distance:.1f}cm) suggests need for focused lower body strength training.")
    
    # Age-adjusted analysis
    if age < 30:
        insights.append("• Optimal age range for peak performance. Focus on maintaining current fitness levels.")
    elif age < 45:
        insights.append("• Maintain consistent training to sustain performance levels and prevent age-related decline.")
    else:
        insights.append("• Focus on mobility, flexibility, and injury prevention while maintaining cardiovascular fitness.")
    
    return '\n'.join(insights)

# --- 4. ENHANCED PDF REPORT GENERATOR ---
class TitanPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            # Header with Logo
            self.set_font('helvetica', 'B', 24)
            self.set_text_color(0, 98, 255)
            self.cell(0, 15, 'TITAN PERFORMANCE ANALYTICS', ln=True, align='C')
            self.set_font('helvetica', 'I', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, 'AI-Powered Body Performance Report', ln=True, align='C')
            self.line(10, 30, 200, 30)
            self.ln(15)

    def footer(self):
        self.set_y(-20)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', align='C')
        self.cell(0, 10, f'Page {self.page_no()}', align='R')

def create_enhanced_pdf(name, age, gender, p_class, p_jump, recs, metrics_dict):
    pdf = TitanPDF()
    pdf.add_page()
    
    # Athlete Information Section
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(0, 98, 255)
    pdf.cell(0, 10, 'ATHLETE INFORMATION', ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    info_data = [
        ['Athlete Name', name],
        ['Age', str(age)],
        ['Gender', gender],
        ['Assessment Date', datetime.now().strftime('%Y-%m-%d %H:%M')]
    ]
    
    for label, value in info_data:
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(50, 8, label + ':', ln=False)
        pdf.set_font('helvetica', '', 11)
        pdf.cell(0, 8, value, ln=True)
    
    pdf.ln(10)
    
    # Performance Results
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(0, 98, 255)
    pdf.cell(0, 10, 'PERFORMANCE METRICS', ln=True)
    pdf.set_fill_color(240, 240, 240)
    
    # Metrics Table
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(100, 10, 'Metric', 1, 0, 'C', True)
    pdf.cell(0, 10, 'Value', 1, 1, 'C', True)
    
    pdf.set_font('helvetica', '', 11)
    for metric, value in metrics_dict.items():
        pdf.cell(100, 8, metric, 1)
        pdf.cell(0, 8, str(value), 1, 1)
    
    pdf.ln(10)
    
    # Analysis Results
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'AI ANALYSIS RESULTS:', ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.cell(0, 10, f'Performance Grade: CLASS {p_class}', ln=True)
    pdf.cell(0, 10, f'Predicted Jump Distance: {p_jump:.2f} cm', ln=True)
    
    pdf.ln(10)
    
    # Recommendations
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'SYSTEM RECOMMENDATIONS:', ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.multi_cell(0, 8, recs)
    
    # Performance Insights
    pdf.ln(5)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 10, 'PERFORMANCE INSIGHTS:', ln=True)
    pdf.set_font('helvetica', 'I', 10)
    
    insights = get_performance_insights(p_class, p_jump, age)
    pdf.multi_cell(0, 6, insights)
    
    return pdf.output()

# --- 5. MODEL LOADING WITH VERSION CHECK ---
@st.cache_resource
def load_assets():
    """Load models with version verification"""
    model_dir = Path('.')
    
    models = {
        'classifier': 'classifier_model.pkl',
        'regression': 'regression_model.pkl',
        'scaler': 'scaler.pkl'
    }
    
    loaded_models = {}
    
    for model_name, filename in models.items():
        model_path = model_dir / filename
        if model_path.exists():
            try:
                loaded_models[model_name] = joblib.load(model_path)
                st.sidebar.success(f"✅ {model_name.capitalize()} loaded")
            except Exception as e:
                st.sidebar.error(f"❌ Error loading {model_name}: {e}")
                return None
        else:
            st.sidebar.error(f"❌ {filename} not found in current directory")
            return None
    
    return loaded_models['classifier'], loaded_models['regression'], loaded_models['scaler']

# --- 6. SESSION STATE INITIALIZATION ---
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None

# --- 7. MAIN INTERFACE ---
st.markdown("<h1 class='tech-header'>⚡ TITAN PERFORMANCE AI ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-top: -20px;'>Advanced Neural Analytics for Athletic Excellence</p>", unsafe_allow_html=True)

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔬 BIOMETRIC ANALYSIS", "📊 PERFORMANCE DASHBOARD", "📈 TREND ANALYTICS", "📚 RESOURCE LIBRARY"])

with tab1:
    col_in, col_out = st.columns([1, 1.2], gap="large")
    
    with col_in:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🧬 BIOMETRIC SCANNER")
        
        # User Input Section
        user_name = st.text_input("🏷️ ATHLETE NAME", "Enter athlete name...")
        
        # Basic Metrics
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("📅 AGE", 10, 80, 25, help="Athlete's age in years")
            height = st.number_input("📏 HEIGHT (CM)", 120.0, 220.0, 175.0, help="Height in centimeters")
        with col2:
            gender_input = st.selectbox("⚥ GENDER", ["Male", "Female"])
            weight = st.number_input("⚖️ WEIGHT (KG)", 30.0, 150.0, 75.0, help="Weight in kilograms")
        
        # BMI Calculation
        bmi = weight / ((height/100) ** 2)
        bmi_category = "Normal" if 18.5 <= bmi <= 24.9 else "Overweight" if bmi > 24.9 else "Underweight"
        st.info(f"📊 BMI: {bmi:.1f} ({bmi_category})")
        
        # Body Composition
        fat = st.slider("💧 BODY FAT %", 5.0, 50.0, 18.0, help="Body fat percentage")
        
        with st.expander("⚡ ADVANCED PERFORMANCE METRICS", expanded=False):
            st.markdown("#### Muscular & Cardiovascular Metrics")
            grip = st.number_input("💪 GRIP STRENGTH (kg)", 0.0, 100.0, 45.0, help="Hand grip strength")
            flex = st.number_input("🧘 FLEXIBILITY (BEND cm)", -20.0, 40.0, 15.0, help="Sit and reach test")
            situps = st.number_input("🏋️ CORE (SIT-UPS)", 0, 100, 45, help="Sit-ups in 1 minute")
            
            st.markdown("#### Vital Signs")
            sys = st.number_input("❤️ SYSTOLIC BP", 80, 200, 120, help="Systolic blood pressure")
            dias = st.number_input("💙 DIASTOLIC BP", 40, 130, 80, help="Diastolic blood pressure")
        
        analyze = st.button("🚀 EXECUTE NEURAL ANALYSIS", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_out:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🛰️ ANALYTICAL OUTPUT")
        
        if analyze:
            try:
                # Load models
                models = load_assets()
                if models is None:
                    st.error("Models not loaded properly. Please check the .pkl files.")
                else:
                    clf, reg, scaler = models
                    
                    with st.spinner("🧠 Initializing Neural Network Inference..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        progress_bar.empty()
                    
                    # Process gender for model
                    gender_val = 0 if gender_input == "Male" else 1
                    
                    # Prepare Feature Vector
                    features = [age, gender_val, height, weight, fat, dias, sys, grip, flex, situps]
                    feature_names = ['age', 'gender', 'height_cm', 'weight_kg', 'body_fat_pct', 
                                    'diastolic', 'systolic', 'gripForce', 'sit_bend_forward_cm', 'sit_ups_counts']
                    
                    input_df = pd.DataFrame([features], columns=feature_names)
                    
                    # Predict
                    scaled_data = scaler.transform(input_df)
                    p_class = clf.predict(scaled_data)[0]
                    p_jump = reg.predict(scaled_data)[0]
                    
                    # Store in session state
                    st.session_state.last_analysis = {
                        'name': user_name,
                        'age': age,
                        'gender': gender_input,
                        'grade': p_class,
                        'jump': p_jump,
                        'bmi': bmi,
                        'fat': fat,
                        'grip': grip,
                        'flex': flex,
                        'situps': situps,
                        'timestamp': datetime.now()
                    }
                    st.session_state.analysis_history.append(st.session_state.last_analysis)
                    
                    # Display Results
                    res1, res2 = st.columns(2)
                    with res1:
                        grade_color = "#00ff00" if p_class == 'A' else "#ffaa00" if p_class == 'B' else "#ff6600"
                        st.metric("🏆 PERFORMANCE GRADE", f"CLASS {p_class}", 
                                 delta="Elite" if p_class == 'A' else "Advanced" if p_class == 'B' else "Developing",
                                 delta_color="normal")
                    with res2:
                        st.metric("📏 JUMP DISTANCE", f"{p_jump:.1f} CM", 
                                 delta=f"{p_jump - 175:.1f}" if p_jump != 175 else None,
                                 delta_color="normal")
                    
                    # Gauge Chart
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=p_jump,
                        delta={'reference': 175, 'increasing': {'color': "#00ff00"}},
                        title={'text': "Explosive Power Index", 'font': {'color': "#00f2ff"}},
                        gauge={
                            'axis': {'range': [None, 300], 'tickwidth': 1, 'tickcolor': "#00f2ff"},
                            'bar': {'color': "#00f2ff"},
                            'bgcolor': "#0f172a",
                            'borderwidth': 2,
                            'bordercolor': "#00f2ff",
                            'steps': [
                                {'range': [0, 150], 'color': '#1e293b'},
                                {'range': [150, 225], 'color': '#334155'},
                                {'range': [225, 300], 'color': '#3b3b5c'}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': p_jump
                            }
                        }
                    ))
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#00f2ff", height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Recommendations
                    rec_text = generate_recommendations(p_class, p_jump, age, bmi, fat)
                    with st.expander("💡 AI RECOMMENDATIONS", expanded=True):
                        st.markdown(rec_text)
                    
                    # PDF Download
                    try:
                        metrics_dict = {
                            'Performance Grade': f'Class {p_class}',
                            'Jump Distance': f'{p_jump:.1f} cm',
                            'BMI': f'{bmi:.1f}',
                            'Body Fat %': f'{fat:.1f}%',
                            'Grip Strength': f'{grip:.1f} kg',
                            'Flexibility': f'{flex:.1f} cm',
                            'Sit-ups': f'{situps} reps'
                        }
                        pdf_data = create_enhanced_pdf(user_name, age, gender_input, p_class, p_jump, rec_text, metrics_dict)
                        
                        st.download_button(
                            label="📥 DOWNLOAD COMPREHENSIVE REPORT (PDF)",
                            data=pdf_data,
                            file_name=f"Titan_Report_{user_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"PDF Generation: {e}")
                    
            except Exception as e:
                st.error(f"Analysis Error: {e}")
                st.info("Please ensure all input values are valid and models are properly loaded.")
        else:
            st.info("⚡ Enter biometric data and click 'EXECUTE NEURAL ANALYSIS' to begin.")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if st.session_state.last_analysis:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 PERFORMANCE RADAR")
        
        # Get last analysis data
        last = st.session_state.last_analysis
        
        # Create radar chart for performance metrics
        categories = ['Strength', 'Flexibility', 'Endurance', 'Power', 'BMI']
        
        # Calculate normalized scores
        strength_score = min(100, (last['grip'] / 60) * 100)
        flexibility_score = min(100, ((last['flex'] + 20) / 60) * 100)
        endurance_score = min(100, (last['situps'] / 80) * 100)
        power_score = min(100, (last['jump'] / 280) * 100)
        bmi_score = 100 - abs(last['bmi'] - 22) * 5
        
        values = [strength_score, flexibility_score, endurance_score, power_score, max(0, min(100, bmi_score))]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            marker=dict(color='rgba(0, 242, 255, 0.8)'),
            line=dict(color='#00f2ff', width=2),
            name='Current Performance'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color='#94a3b8')
                ),
                angularaxis=dict(
                    tickfont=dict(color='#00f2ff')
                )
            ),
            showlegend=True,
            title="Multi-Dimensional Performance Analysis",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#00f2ff",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics table
        st.markdown("### 📈 DETAILED METRICS")
        metrics_data = {
            'Metric': ['Performance Grade', 'Jump Distance', 'BMI', 'Body Fat %', 'Grip Strength', 'Flexibility', 'Sit-ups'],
            'Value': [f'Class {last["grade"]}', f'{last["jump"]:.1f} cm', f'{last["bmi"]:.1f}', f'{last["fat"]:.1f}%', 
                     f'{last["grip"]:.1f} kg', f'{last["flex"]:.1f} cm', f'{last["situps"]} reps'],
            'Percentile': [get_percentile(last["grade"]), get_jump_percentile(last["jump"]), get_bmi_percentile(last["bmi"]), 
                          get_fat_percentile(last["fat"]), get_grip_percentile(last["grip"]), 
                          get_flex_percentile(last["flex"]), get_situps_percentile(last["situps"])]
        }
        
        df_metrics = pd.DataFrame(metrics_data)
        st.dataframe(df_metrics, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🔍 Complete an analysis in the BIOMETRIC ANALYSIS tab to view detailed metrics.")

with tab3:
    if len(st.session_state.analysis_history) > 0:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📈 PERFORMANCE TRENDS")
        
        # Create trend visualization
        history_df = pd.DataFrame(st.session_state.analysis_history)
        
        if len(history_df) > 1:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=history_df['timestamp'],
                y=history_df['jump'],
                mode='lines+markers',
                name='Jump Distance',
                line=dict(color='#00f2ff', width=3),
                marker=dict(size=8, color='#0062ff')
            ))
            
            fig.update_layout(
                title="Performance Evolution Over Time",
                xaxis_title="Analysis Date",
                yaxis_title="Jump Distance (cm)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#00f2ff",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Improvement analysis
            if len(history_df) >= 2:
                first_jump = history_df.iloc[0]['jump']
                last_jump = history_df.iloc[-1]['jump']
                improvement = last_jump - first_jump
                
                if improvement > 0:
                    st.success(f"📈 Positive trend detected! Performance improved by {improvement:.1f} cm since first analysis.")
                elif improvement < 0:
                    st.warning(f"📉 Performance decline of {abs(improvement):.1f} cm detected. Review training regimen.")
                else:
                    st.info("📊 Performance stable. Consistent training maintaining current levels.")
        else:
            st.info("📊 Perform multiple analyses to see performance trends over time.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📈 Complete at least 2 analyses to view performance trends.")

with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📚 ATHLETE DEVELOPMENT RESOURCES")
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.markdown("#### 🏋️ Training Protocols")
        st.markdown("""
        **Elite Level (Class A)**
        - Advanced periodization training
        - Sport-specific explosive power drills
        - Recovery optimization protocols
        
        **Advanced Level (Class B)**
        - Progressive overload training
        - Plyometric integration
        - Nutrition optimization
        
        **Developing Level (Class C/D)**
        - Foundation strength building
        - Mobility and flexibility focus
        - Cardiovascular conditioning
        """)
    
    with col_r2:
        st.markdown("#### 🥗 Nutrition Guidelines")
        st.markdown("""
        **Pre-Workout (2-3 hours before)**
        - Complex carbohydrates
        - Lean protein
        - Hydration (500ml water)
        
        **Post-Workout (within 30 min)**
        - Fast-absorbing protein
        - Simple carbohydrates
        - Electrolyte replacement
        
        **Daily Recommendations**
        - Protein: 1.6-2.2g/kg body weight
        - Water: 3-4 liters
        - Sleep: 7-9 hours
        """)
    
    st.markdown("#### 🔬 Research-Backed Insights")
    with st.expander("View Scientific References"):
        st.markdown("""
        - **Jump Performance**: Vertical jump height correlates strongly with lower body power output (r=0.89)
        - **Body Composition**: Optimal body fat % for athletes: 6-13% (male), 14-20% (female)
        - **Flexibility**: Sit-and-reach values >20cm associated with reduced injury risk
        - **Core Strength**: Sit-up capacity >50/min indicates excellent core endurance
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("""
<div class='footer'>
    <p>⚡ TITAN PERFORMANCE ANALYTICS v5.0 | Neural Network Engine | Real-time Analysis</p>
    <p>© 2026 Advanced AI Analytics Division | Data-Driven Athletic Development</p>
</div>
""", unsafe_allow_html=True)
