import streamlit as st

st.set_page_config(page_title="Body Performance AI", layout="wide")

st.title("⚡ Body Performance AI Pro")
st.write("Testing Streamlit setup...")

# تحقق من المكتبات
try:
    import pandas as pd
    st.success("✅ Pandas loaded")
except:
    st.error("❌ Pandas not found")

try:
    import numpy as np
    st.success("✅ NumPy loaded")
except:
    st.error("❌ NumPy not found")

try:
    import plotly.express as px
    st.success("✅ Plotly loaded")
except:
    st.error("❌ Plotly not found")

st.info("If you see this, Streamlit is working correctly!")

# اختبار بسيط
if st.button("Test Button"):
    st.balloons()
    st.write("Application is running!")
