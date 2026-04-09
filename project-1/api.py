from fastapi import FastAPI
from main import DataEngine
import pandas as pd

app = FastAPI(title="Online Retail API", description="REST API for E-Commerce Analysis")
engine = DataEngine()

# Pre-load and clean data for fast serving
try:
    engine.clean_data()
except Exception as e:
    print(f"Warning: Data loading failed: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Retail Analysis API", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "data_loaded": engine.df is not None}

@app.get("/summary")
def get_summary():
    """Returns general business KPIs."""
    if engine.df is None:
        return {"error": "Data not loaded"}
    return engine.get_summary_stats()

@app.get("/sales-by-country")
def get_country_sales(exclude_uk: bool = True):
    """Returns revenue grouped by country."""
    if engine.df is None:
        return {"error": "Data not loaded"}
    
    sales = engine.get_sales_by_country(exclude_uk=exclude_uk)
    # Convert series to dictionary for JSON response
    return sales.to_dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
