import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from PIL import Image
from sklearn.datasets import fetch_openml

# 1. Page Configuration
st.set_page_config(
    page_title="CardioGuard AI | Heart Disease Diagnosis",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Premium Styling
st.markdown("""
    <style>
    /* Gradient Background for Header */
    .main {
        background-color: #0e1117;
    }
    .stApp {
        color: #ffffff;
    }
    h1 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(#FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    div[data-testid="stSidebar"] {
        background-color: #1a1c24;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Data Loading (For Statistics)
@st.cache_data
def load_analysis_data():
    """Fetch data for statistical analysis."""
    dataset = fetch_openml(data_id=45547, as_frame=True, parser='auto')
    df = dataset.frame.copy()
    
    # Fix: Ensure all clinical columns are numeric (prevents aggregation TypeErrors)
    cols_to_fix = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                   'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']
    for col in cols_to_fix:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Preprocessing identical to main.py
    df['age'] = (df['age'] / 365.25).round().astype(int)
    df = df[(df['ap_hi'] >= 50) & (df['ap_hi'] <= 250)]
    df = df[(df['ap_lo'] >= 40) & (df['ap_lo'] <= 180)]
    df = df[df['ap_hi'] > df['ap_lo']]
    df['bmi'] = (df['weight'] / ((df['height']/100)**2)).round(1)
    return df

analysis_df = load_analysis_data()

# 3. Load Model
@st.cache_resource
def load_production_model():
    if os.path.exists('cardio_model.joblib'):
        return joblib.load('cardio_model.joblib')
    return None

package = load_production_model()

# 5. Sidebar Inputs
st.sidebar.title("🩺 Patient Vitals")
st.sidebar.markdown("---")

with st.sidebar:
    st.subheader("Demographics")
    age = st.slider("Age (Years)", 1, 100, 50)
    gender = st.selectbox("Gender", ["Female", "Male"])
    height = st.number_input("Height (cm)", 50, 250, 170)
    weight = st.number_input("Weight (kg)", 10, 300, 70)
    
    st.markdown("---")
    st.subheader("Clinical Metrics")
    ap_hi = st.slider("Systolic BP (High)", 50, 250, 120)
    ap_lo = st.slider("Diastolic BP (Low)", 40, 180, 80)
    
    cholesterol = st.selectbox("Cholesterol Level", 
                               options=[1, 2, 3],
                               format_func=lambda x: ["Normal", "Above Normal", "High"][x-1])
    
    gluc = st.selectbox("Glucose Level", 
                        options=[1, 2, 3],
                        format_func=lambda x: ["Normal", "Above Normal", "High"][x-1])

    st.markdown("---")
    st.subheader("Lifestyle")
    smoke = st.checkbox("Smoker")
    alco = st.checkbox("Alcohol Intake")
    active = st.checkbox("Physically Active")

# 6. Main Content Area
st.title("CardioGuard AI Dashboard")
st.markdown("##### Real-time Clinical Heart Disease Risk Assessment")

if package is None:
    st.error("❌ Production model not found! Please run 'main.py' first to train the model.")
else:
    model = package['model']
    features = package['features']
    
    # Calculate BMI locally for the model
    bmi = round(weight / ((height/100)**2), 1)
    
    # Prepare Input Data
    # Feature ordering must match training: age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, bmi
    input_data = pd.DataFrame([[
        age, 
        2 if gender == "Male" else 1, 
        height, 
        weight, 
        ap_hi, 
        ap_lo, 
        cholesterol, 
        gluc, 
        1 if smoke else 0, 
        1 if alco else 0, 
        1 if active else 0, 
        bmi
    ]], columns=features)
    
    # Header Statistics
    col1, col2, col3 = st.columns(3)
    
    # 6. Prediction Logic
    prob = model.predict_proba(input_data)[0][1]
    risk_level = "HIGH" if prob > 0.5 else "LOW"
    risk_color = "red" if prob > 0.5 else "green"
    
    with col1:
        st.metric("Risk Probability", f"{prob*100:.1f}%")
    with col2:
        st.metric("Diagnostic Result", risk_level, delta="Positive" if risk_level == "HIGH" else "Negative", delta_color="inverse")
    with col3:
        st.metric("Computed BMI", bmi)

    # 7. Visualized Verdict
    st.markdown(f"""
        <div style="background-color:{risk_color}; padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:white; margin:0;">Verdict: {risk_level} HEART DISEASE RISK</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 8. Clinical Insights Section
    tabs = st.tabs(["📊 Diagnostic Insights", "🔍 Deep-Dive Analytics", "📈 Population Trends", "📄 Dataset Viewer", "📋 Patient Summary"])
    
    with tabs[0]:
# ... (Diagnostic Insights code)
        st.subheader("Model Decision Logic")
        st.info("The charts below represent the population-wide intelligence used by this model.")
        col_img1, col_img2 = st.columns(2)
        
        if os.path.exists('clinical_feature_importance.png'):
            col_img1.image('clinical_feature_importance.png', caption="Most Critical Medical Indicators")
        if os.path.exists('confusion_matrix_large.png'):
            col_img2.image('confusion_matrix_large.png', caption="Model Confusion Matrix (Validation)")

    with tabs[1]:
# ... (Deep-Dive Analytics code)
        st.subheader("Precision Analysis: Cardiac vs Healthy Groups")
        
        # 1. Comparison Table
        group_stats = analysis_df.groupby('cardio')[['age', 'ap_hi', 'ap_lo', 'bmi', 'cholesterol']].mean().T
        group_stats.columns = ['Healthy Group', 'Cardiac Group']
        group_stats['Difference (%)'] = ((group_stats['Cardiac Group'] - group_stats['Healthy Group']) / group_stats['Healthy Group'] * 100).round(1)
        st.table(group_stats)
        
        # 2. Category Analysis
        col_st1, col_st2 = st.columns(2)
        
        with col_st1:
            st.markdown("**Risk by Blood Pressure Category**")
            # WHO BP Categories
            def categorize_bp(row):
                if row['ap_hi'] < 120 and row['ap_lo'] < 80: return 'Normal'
                elif row['ap_hi'] < 130 and row['ap_lo'] < 80: return 'Elevated'
                elif row['ap_hi'] < 140 or row['ap_lo'] < 90: return 'Hypertension S1'
                else: return 'Hypertension S2'
            
            analysis_df['bp_category'] = analysis_df.apply(categorize_bp, axis=1)
            bp_analysis = analysis_df.groupby('bp_category')['cardio'].mean() * 100
            st.bar_chart(bp_analysis)
            
        with col_st2:
            st.markdown("**Risk by BMI Category**")
            bins = [0, 18.5, 25, 30, 100]
            labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
            analysis_df['bmi_class'] = pd.cut(analysis_df['bmi'], bins=bins, labels=labels)
            bmi_analysis = analysis_df.groupby('bmi_class', observed=False)['cardio'].mean() * 100
            st.bar_chart(bmi_analysis)

    with tabs[2]:
        st.subheader("Correlation Analysis")
        if os.path.exists('correlation_heatmap_large.png'):
            st.image('correlation_heatmap_large.png', use_container_width=True)

    with tabs[3]:
        st.subheader("Interactive Patient Record Explorer")
        st.markdown(f"Displaying all **{len(analysis_df)}** cleaned clinical records.")
        
        # Download Button
        csv = analysis_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned Dataset (CSV)",
            data=csv,
            file_name='cleaned_cardio_data.csv',
            mime='text/csv',
        )
        
        # Searchable Dataframe
        st.dataframe(analysis_df, use_container_width=True)

    with tabs[4]:
        st.subheader("Patient Clinical Profile")
        st.write(input_data)
        
st.markdown("---")
st.caption("Disclaimer: This tool is for educational purposes and project demonstration only. Always consult a medical professional for actual diagnosis.")
