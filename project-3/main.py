import pandas as pd
import numpy as np

def load_data():
    file_path = "Telco-Customer-Churn.csv"
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    df_clean = df.copy()
    # TotalCharges is object due to blank strings ' '
    df_clean['TotalCharges'] = df_clean['TotalCharges'].replace(' ', np.nan)
    df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'])
    # Drop rows with NaN (only 11 rows)
    df_clean = df_clean.dropna()
    return df_clean
