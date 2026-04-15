import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Import logic from main.py
from main import load_offline_data, prepare_features, train_predictive_model

st.set_page_config(page_title="Stock Market Insights & Prediction", layout="wide")

st.title("📈 Real-World Data Project: Stock Market Insights")
st.markdown("An interactive dashboard to analyze historical stock data and predict future prices using Random Forest.")

# --- Sidebar Inputs ---
st.sidebar.header("User Inputs")
data_file = st.sidebar.file_uploader("Choose Offline Dataset (CSV)", type=['csv'])
st.sidebar.info("By default, it uses the downloaded AAPL_stock_data.csv.")

with st.spinner("Loading offline data..."):
    if data_file is not None:
        df = load_offline_data(data_file)
        ticker = "Uploaded Data"
    else:
        df = load_offline_data("AAPL_stock_data.csv")
        ticker = "AAPL"
        
if df.empty:
    st.error("Failed to load dataset. Please ensure the CSV is properly formatted.")
else:
    st.success("Offline Data loaded successfully!")
    
    # --- Exploratory Data Analysis (EDA) ---
    st.header(f"1. Exploratory Data Analysis: {ticker}")
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Real-World Dataset (CSV)",
        data=csv_data,
        file_name=f"{ticker}_dataset.csv",
        mime="text/csv",
    )
    
    col1, col2, col3 = st.columns(3)
    latest_close = df['Close'].iloc[-1].item() if isinstance(df['Close'].iloc[-1], pd.Series) else df['Close'].iloc[-1]
    previous_close = df['Close'].iloc[-2].item() if isinstance(df['Close'].iloc[-2], pd.Series) else df['Close'].iloc[-2]
    delta = latest_close - previous_close
    
    col1.metric("Latest Close Price", f"${latest_close:.2f}", f"{delta:.2f}")
    col2.metric("Total Trading Days", len(df))
    avg_vol = df['Volume'].mean().item() if isinstance(df['Volume'].mean(), pd.Series) else df['Volume'].mean()
    col3.metric("Average Volume", f"{avg_vol:,.0f}")
    
    # Time Series Plot
    st.subheader("Historical Closing Prices")
    fig_hist = px.line(df, x='Date', y='Close', title=f"{ticker} Closing Price Over Time")
    fig_hist.update_xaxes(title_text='Date')
    fig_hist.update_yaxes(title_text='Closing Price ($)')
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Histogram for Volume
    st.subheader("Volume Distribution")
    fig_vol = px.histogram(df, x='Volume', nbins=50, title=f"{ticker} Volume Distribution")
    st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown("### EDA Conclusions")
    st.info("The exploratory phase helps us understand general trends, price volatility, and volume spikes over periods of market activity.")
    
    # --- Predictive Modeling ---
    st.header("2. Predictive Modeling (Random Forest)")
    st.markdown("We process the historical data by calculating **10-day and 50-day Simple Moving Averages (SMA)** and **lag features** to build a robust model to predict the *next day's* close price.")
    
    with st.spinner("Training predictive model..."):
        prep_df = prepare_features(df)
        if len(prep_df) < 50:
            st.warning("Not enough data to train the model after calculating moving averages. Increase the date range.")
        else:
            results_df, metrics = train_predictive_model(prep_df)
            
            # Model Metrics
            st.subheader("Model Performance Evaluation")
            c1, c2, c3 = st.columns(3)
            c1.metric("Mean Absolute Error (MAE)", f"${metrics['MAE']:.3f}")
            c2.metric("Mean Squared Error (MSE)", f"${metrics['MSE']:.3f}")
            c3.metric("R² Score", f"{metrics['Accuracy_Score_approx']:.4f}")
            
            # Visualization of Actual vs. Predicted
            st.subheader("Test Data: Actual vs. Predicted Next-Day Prices")
            
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(x=results_df['Date'], y=results_df['Actual_Next_Close'], mode='lines', name='Actual Price'))
            fig_pred.add_trace(go.Scatter(x=results_df['Date'], y=results_df['Predicted_Next_Close'], mode='lines', name='Predicted Price', line=dict(dash='dot')))
            
            fig_pred.update_layout(title="Prediction Accuracy on Test Set (Last 20% of timeline)", xaxis_title="Date", yaxis_title="Price ($)")
            st.plotly_chart(fig_pred, use_container_width=True)
            
            st.markdown("### Modeling Conclusions")
            st.success("The Random Forest Regressor demonstrates the ability to capture general trends, despite the inherent volatility of stock prices. Using Moving Averages and Lag features significantly assists the model's predictive power.")
