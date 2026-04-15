import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ----------------------------------------------------------------------------
# 1. SETUP AND CONFIGURATION
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Telco Churn Analytics",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a beautiful, premium theme
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 2. DATA LOADING & PREPROCESSING
# ----------------------------------------------------------------------------
from main import load_data, preprocess_data

@st.cache_data
def get_data():
    raw = load_data()
    clean = preprocess_data(raw)
    return raw, clean

# Load Data
df_raw, df = get_data()

# ----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# ----------------------------------------------------------------------------
st.sidebar.title("📡 Navigation")
pages = [
    "📋 Overview & Statistics", 
    "👨‍👩‍👧‍👦 Demographics Analysis", 
    "📶 Services Analysis", 
    "💰 Financial Analysis",
    "🔗 Correlations"
]
selection = st.sidebar.radio("Go to", pages)

st.sidebar.markdown("---")
st.sidebar.info("This dashboard explores the IBM Telco Customer Churn dataset to uncover patterns in customer retention.")

# ----------------------------------------------------------------------------
# 4. PAGE IMPLEMENTATIONS
# ----------------------------------------------------------------------------

if selection == "📋 Overview & Statistics":
    st.title("📋 Dataset Overview & Statistics")
    st.markdown("Explore the raw data and high-level statistical summaries.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", len(df))
    with col2:
        st.metric("Total Features", len(df.columns))
    with col3:
        churn_rate = (len(df[df['Churn'] == 'Yes']) / len(df)) * 100
        st.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
    with col4:
        avg_tenure = df['tenure'].mean()
        st.metric("Average Tenure (Months)", f"{avg_tenure:.1f}")

    st.markdown("### Preview of Data")
    st.dataframe(df.head(10))
    
    st.markdown("### Descriptive Statistics (Numeric)")
    st.dataframe(df.describe().T)

    st.markdown("### Missing Values Analysis")
    missing_data = df_raw.isnull().sum()
    st.write("Original missing values: None, except blank strings in `TotalCharges` (11 rows). Handled in preprocessing.")

elif selection == "👨‍👩‍👧‍👦 Demographics Analysis":
    st.title("👨‍👩‍👧‍👦 Demographics Analysis")
    st.markdown("How do gender, age, and family status affect churn?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Churn by Gender
        fig_gender = px.histogram(df, x='gender', color='Churn', barmode='group', 
                                title='Churn by Gender', color_discrete_sequence=['#38BDF8', '#F43F5E'])
        st.plotly_chart(fig_gender)
        
        # Churn by Senior Citizen
        df['SeniorCitizen_Status'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
        fig_senior = px.histogram(df, x='SeniorCitizen_Status', color='Churn', barmode='group', 
                                title='Churn by Senior Citizen', color_discrete_sequence=['#38BDF8', '#F43F5E'])
        st.plotly_chart(fig_senior)
        
    with col2:
        # Churn by Partner
        fig_partner = px.histogram(df, x='Partner', color='Churn', barmode='group', 
                                title='Churn by Partner Status', color_discrete_sequence=['#38BDF8', '#F43F5E'])
        st.plotly_chart(fig_partner)
        
        # Churn by Dependents
        fig_dep = px.histogram(df, x='Dependents', color='Churn', barmode='group', 
                            title='Churn by Dependents Status', color_discrete_sequence=['#38BDF8', '#F43F5E'])
        st.plotly_chart(fig_dep)
        
    st.info("Insights: Customers without partners or dependents, and senior citizens, show a higher propensity to churn.")

elif selection == "📶 Services Analysis":
    st.title("📶 Services Analysis")
    st.markdown("Impact of internet, phone, and add-on services on churn.")
    
    tab1, tab2 = st.tabs(["Core Services", "Add-On Services"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig_internet = px.histogram(df, x='InternetService', color='Churn', barmode='group', 
                                    title='Churn by Internet Service', color_discrete_sequence=['#10B981', '#EF4444'])
            st.plotly_chart(fig_internet)
        with col2:
            fig_phone = px.histogram(df, x='PhoneService', color='Churn', barmode='group', 
                                    title='Churn by Phone Service', color_discrete_sequence=['#10B981', '#EF4444'])
            st.plotly_chart(fig_phone)

    with tab2:
        services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport']
        for i in range(0, 4, 2):
            colA, colB = st.columns(2)
            with colA:
                fig = px.histogram(df, x=services[i], color='Churn', barmode='group', 
                                title=f'Churn by {services[i]}', color_discrete_sequence=['#8B5CF6', '#F59E0B'])
                st.plotly_chart(fig)
            with colB:
                fig2 = px.histogram(df, x=services[i+1], color='Churn', barmode='group', 
                                title=f'Churn by {services[i+1]}', color_discrete_sequence=['#8B5CF6', '#F59E0B'])
                st.plotly_chart(fig2)

    st.info("Insights: Customers with Fiber Optic internet have extremely high churn. Conversely, having Tech Support or Online Security severely drops the churn rate.")

elif selection == "💰 Financial Analysis":
    st.title("💰 Financial & Contract Analysis")
    st.markdown("How do contracts, payment methods, and charges influence customer retention?")
    
    # Contract
    st.markdown("### Contract Types")
    fig_contract = px.histogram(df, x='Contract', color='Churn', barmode='group', 
                               title='Churn by Contract Type', color_discrete_sequence=['#F59E0B', '#3B82F6'])
    st.plotly_chart(fig_contract)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        # Monthly Charges Dist
        fig_monthly = px.box(df, x='Churn', y='MonthlyCharges', color='Churn',
                           title='Distribution of Monthly Charges', color_discrete_sequence=['#F59E0B', '#3B82F6'])
        st.plotly_chart(fig_monthly)
    with col2:
        # Total Charges Dist
        fig_total = px.box(df, x='Churn', y='TotalCharges', color='Churn',
                         title='Distribution of Total Charges', color_discrete_sequence=['#F59E0B', '#3B82F6'])
        st.plotly_chart(fig_total)

    st.markdown("### Payment Method")
    fig_payment = px.histogram(df, y='PaymentMethod', color='Churn', barmode='group', orientation='h',
                              title='Churn by Payment Method', color_discrete_sequence=['#F59E0B', '#3B82F6'])
    st.plotly_chart(fig_payment)
    
    st.warning("Note: Customers on Month-to-Month contracts and those using Electronic Checks are far more likely to leave.")

elif selection == "🔗 Correlations":
    st.title("🔗 Correlation Analysis")
    st.markdown("Mathematical linear relationships between numerical variables and churn.")
    
    # Selecting numeric columns
    numeric_df = df.select_dtypes(include=[np.number]).copy()
    
    # Adding a numeric representation of Churn to see what drives it
    numeric_df['Churn_Numeric'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # Calculate correlation matrix
    corr = numeric_df.corr()
    
    # Plotly heatmap
    fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", 
                         color_continuous_scale="RdBu_r",
                         title="Pearson Correlation Heatmap")
    st.plotly_chart(fig_corr)
    
    st.info("Insights: `tenure` and `TotalCharges` are highly positively correlated. `Churn_Numeric` has a negative correlation with `tenure` (longer stay = less likely to leave) and a positive correlation with `MonthlyCharges` (higher monthly bill = more likely to leave).")
