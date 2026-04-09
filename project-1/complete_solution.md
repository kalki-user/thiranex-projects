# 🚀 Complete Project Solution: Online Retail Analysis

This document contains the full, ready-to-run Python code for the project. You can copy this into your `main.py` or a new file to see the complete results.

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. LOAD DATA ---
LOCAL_PATH = 'data/raw/online_retail_real.csv'

if not os.path.exists(LOCAL_PATH):
    print("Error: Local data file not found. Please run the initial download script first.")
else:
    print(f"Loading data: {LOCAL_PATH}")
    df = pd.read_csv(LOCAL_PATH, encoding='ISO-8859-1')

    # --- STEP 1: INITIAL DATA CLEANING ---
    print("Cleaning data...")
    # Remove cancellations (InvoiceNo starts with 'C')
    df = df[~df['InvoiceNo'].str.contains('C', na=False)]

    # Remove rows with negative or zero quantities/unit prices
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # Handle Missing CustomerIDs (fill with 0 as 'Guest')
    df['CustomerID'] = df['CustomerID'].fillna(0)

    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # --- STEP 2: FEATURE ENGINEERING ---
    print("Calculating metrics...")
    # Calculate Total Sales (Revenue)
    df['TotalSales'] = df['Quantity'] * df['UnitPrice']

    # Extract Month and Year for trends
    df['Month'] = df['InvoiceDate'].dt.month
    df['Year'] = df['InvoiceDate'].dt.year
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')

    # --- STEP 3: DATA AGGREGATION ---
    print("Aggregating results...")
    # Monthly Revenue Trend
    monthly_sales = df.groupby('YearMonth')['TotalSales'].sum()

    # Sales by Country (Top 10 excluding UK for better visibility)
    country_sales = df[df['Country'] != 'United Kingdom'].groupby('Country')['TotalSales'].sum().sort_values(ascending=False).head(10)

    # Top 10 Products by Revenue
    top_products = df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(10)

    # --- STEP 4: VISUALIZATION ---
    print("Generating plots...")
    plt.style.use('seaborn-v0_8-muted') # Set a nice aesthetic
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))

    # Plot 1: Monthly Sales Trend
    monthly_sales.plot(kind='line', marker='o', ax=axes[0], color='#eb4d4b', linewidth=2)
    axes[0].set_title('Global Monthly Sales Trend (Dec 2010 - Dec 2011)', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Total Revenue ($)', fontsize=12)
    axes[0].grid(True, linestyle='--', alpha=0.7)

    # Plot 2: Top 10 Countries by Revenue (Excl. UK)
    country_sales.plot(kind='bar', ax=axes[1], color='#686de0')
    axes[1].set_title('Top 10 Countries by Revenue (Excluding UK)', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Total Revenue ($)', fontsize=12)
    plt.xticks(rotation=45)

    plt.tight_layout()
    
    # Save the dashboard
    if not os.path.exists('outputs/plots'):
        os.makedirs('outputs/plots')
    plt.savefig('outputs/plots/analysis_dashboard.png')
    print("Dashboard saved to: outputs/plots/analysis_dashboard.png")
    
    plt.show()

    # --- STEP 5: FINAL INSIGHTS ---
    print("\n" + "="*30)
    print("       FINAL INSIGHTS")
    print("="*30)
    print(f"Total Transactions Analyzed: {len(df):,}")
    print(f"Total Revenue Generated: ${df['TotalSales'].sum():,.2f}")
    print(f"Top Non-UK Market: {country_sales.index[0]} (${country_sales.iloc[0]:,.2f})")
    print(f"Best Performing Month: {monthly_sales.idxmax()} (${monthly_sales.max():,.2f})")
    print("="*30)
```

## How to use this code:
1. **Copy** the code block above.
2. **Paste** it into your `main.py` (replacing everything).
3. **Run** it using `python main.py`.
4. **Result**: Your console will show the insights, a window will pop up with the charts, and a high-resolution dashboard will be saved in your `outputs/` folder.
