# CardioGuard AI: Clinical Heart Disease Prediction

An enterprise-grade machine learning system designed to predict cardiovascular disease risk using clinical parameters. This project utilizes a large-scale dataset of **70,000 patient records** from Kaggle to build a highly robust Random Forest diagnostic model.

## 🚀 Overview
CardioGuard AI transforms raw clinical data into actionable medical intelligence. It provides both a backend training pipeline and an interactive, real-time diagnostic dashboard for healthcare practitioners.

### Key Features
- **Massive Data Scale**: Trained on 70,000 real-world records.
- **Ensemble Learning**: Uses a Random Forest Classifier for stable and accurate medical predictions (~73% validation accuracy).
- **Deep Analytics**: WHO-aligned blood pressure categorization and BMI risk stratification.
- **Interactive Dashboard**: Real-time risk scoring, feature importance visualization, and raw data exploration.
- **Production Ready**: Exported model (`.joblib`) ready for integration into hospital management systems.

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **Machine Learning**: Scikit-Learn (Random Forest)
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Seaborn, Matplotlib
- **Web Interface**: Streamlit

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model (Backend)
This script fetches the 70k Kaggle records via OpenML, cleans the data, and exports the model.
```bash
python main.py
```

### 3. Launch the Dashboard (Frontend)
Initialize the interactive clinical interface.
```bash
streamlit run app.py
```

## 📊 Methodology & Findings
The model identifies **Systolic Blood Pressure (ap_hi)** and **Age** as the most significant predictors of cardiovascular health in this population.

### Data Cleaning Note
Original Kaggle data contains noise (e.g., negative BP values or impossible BP > 300). This project includes a sophisticated `DataCleaner` pipeline that filters records to realistic clinical ranges (SBP: 50-250, DBP: 40-180) to ensure model integrity.

## 📄 License
This project is for educational and research purposes. Medical decisions should only be made by licensed professionals.
