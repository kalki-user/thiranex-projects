import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.datasets import fetch_openml
import os
import joblib

# Set visual aesthetics
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

class HeartDiseasePipeline:
    def __init__(self, data_id=45547):
        self.data_id = data_id
        self.model = None
        self.feature_names = None
        self.df = None

    def fetch_data(self):
        """Fetch the Cardiovascular Disease dataset from OpenML."""
        print(f"\n[1/6] Fetching dataset (ID: {self.data_id}) from OpenML...")
        try:
            # parser='auto' is efficient for large datasets
            dataset = fetch_openml(data_id=self.data_id, as_frame=True, parser='auto')
            self.df = dataset.frame
            print(f"--- Dataset Loaded: {self.df.shape[0]} records, {self.df.shape[1]} features ---")
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False

    def preprocess_data(self):
        """Clean and transform the raw data."""
        print("\n[2/6] Preprocessing and Cleaning data...")
        
        # 1. Convert age from days to years
        self.df['age'] = (self.df['age'] / 365.25).round().astype(int)
        
        # 2. Filter Blood Pressure outliers (Real-world clinical ranges: 50-250)
        # This is CRITICAL for real datasets as they often contain 'zero' or 'typo' BP values
        initial_count = len(self.df)
        self.df = self.df[(self.df['ap_hi'] >= 50) & (self.df['ap_hi'] <= 250)]
        self.df = self.df[(self.df['ap_lo'] >= 40) & (self.df['ap_lo'] <= 180)]
        
        # Ensure systolic is greater than diastolic
        self.df = self.df[self.df['ap_hi'] > self.df['ap_lo']]
        
        removed = initial_count - len(self.df)
        print(f"--- Cleaned {removed} noisy records (BP outliers). Remaining: {len(self.df)} ---")
        
        # 3. Simple Feature Engineering: Calculate BMI
        self.df['bmi'] = (self.df['weight'] / ((self.df['height']/100)**2)).round(1)
        
        print(self.df.head())

    def perform_eda(self):
        """Generate high-quality visualizations."""
        print("\n[3/6] Performing Exploratory Data Analysis (EDA)...")
        
        # Relationship between Age and Cardiovascular Disease
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df, x="age", hue="cardio", multiple="stack", bins=20, palette="magma")
        plt.title("Cardiovascular Disease Prevalence by Age", fontsize=16)
        plt.savefig('age_distribution_analysis.png')
        
        # Correlation Matrix
        plt.figure(figsize=(12, 10))
        corr = self.df.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', center=0)
        plt.title('Patient Feature Correlation Heatmap', fontsize=16)
        plt.savefig('correlation_heatmap_large.png')
        
        print("--- EDA Complete. Saved 'age_distribution_analysis.png' and 'correlation_heatmap_large.png' ---")

    def train_model(self):
        """Train the Random Forest Classifier."""
        print("\n[4/6] Training Random Forest Model (Optimized for 70k records)...")
        
        X = self.df.drop('cardio', axis=1)
        y = self.df['cardio'].astype(int)
        self.feature_names = X.columns.tolist()
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # We use n_jobs=-1 to utilize all CPU cores for the large dataset
        self.model = RandomForestClassifier(n_estimators=100, max_depth=15, min_samples_split=20, n_jobs=-1, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        print(f"--- Model Trained! Validation Accuracy: {acc*100:.2f}% ---")
        
        # Model Evaluation
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Disease Prediction Confusion Matrix')
        plt.savefig('confusion_matrix_large.png')
        
        return acc

    def visualize_importance(self):
        """Show which medical factors matter most."""
        print("\n[5/6] Analyzing Feature Importance...")
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(12, 8))
        sns.barplot(x=importances[indices], y=[self.feature_names[i] for i in indices], palette='viridis')
        plt.title("Key Clinical Indicators of Cardiovascular Disease", fontsize=18)
        plt.xlabel('Importance Score')
        plt.savefig('clinical_feature_importance.png')
        print("--- Feature Importance saved to 'clinical_feature_importance.png' ---")

    def export_model(self, filename='cardio_model.joblib'):
        """Save the model for future use in production."""
        print(f"\n[6/6] Exporting production model to {filename}...")
        joblib.dump({
            'model': self.model,
            'features': self.feature_names
        }, filename)
        print("--- Deployment Package Ready! ---")

if __name__ == "__main__":
    pipeline = HeartDiseasePipeline()
    
    if pipeline.fetch_data():
        pipeline.preprocess_data()
        pipeline.perform_eda()
        pipeline.train_model()
        pipeline.visualize_importance()
        pipeline.export_model()
        
        print("\n" + "="*50)
        print(" MEDICAL DIAGNOSIS PROJECT COMPLETE (KAGGLE DATASET) ")
        print("="*50)
        print("Files Generated:")
        print("1. age_distribution_analysis.png")
        print("2. correlation_heatmap_large.png")
        print("3. confusion_matrix_large.png")
        print("4. clinical_feature_importance.png")
        print("5. cardio_model.joblib (Production Model)")
