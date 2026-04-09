# 📊 Online Retail Data Analysis Project

This project focuses on transforming a raw, messy dataset of over 540,000 transactions into a clean, actionable business intelligence report.

---

## 🚀 Project Roadmap & Explanations

### Step 1: Initial Data Cleaning
**Objective:** Create a "Golden Dataset" that is free from errors and outliers.
*   **Filter Cancellations**: Orders starting with 'C' represent returns.
    ```python
    df = df[~df['InvoiceNo'].str.contains('C', na=False)]
    ```
*   **Missing CustomerIDs**: We'll keep them but treat them as "Guest" checkouts.
    ```python
    df['CustomerID'] = df['CustomerID'].fillna(0)
    ```
*   **Date Conversion**: Convert strings to proper datetime objects.
    ```python
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    ```

### Step 2: Feature Engineering
**Objective:** Add new columns to the data to unlock deeper insights.
*   **TotalSales**: The money earned from each line item.
    ```python
    df['TotalSales'] = df['Quantity'] * df['UnitPrice']
    ```
*   **Time Features**: Breaking the date into chunks.
    ```python
    df['Month'] = df['InvoiceDate'].dt.month
    ```

### Step 3: Data Aggregation
**Objective:** Summarize the massive 540,000 rows into small, readable tables.
*   **Sales by Country**:
    ```python
    country_revenue = df.groupby('Country')['TotalSales'].sum().sort_values(ascending=False)
    ```

### Step 4: Visual Storytelling
**Objective:** Turn numbers into pictures.
*   **Line Chart Example**:
    ```python
    df.groupby('Month')['TotalSales'].sum().plot(kind='line')
    plt.title('Monthly Sales Trend')
    plt.show()
    ```

### Step 5: Final Insights
**Objective:** Answer the "So What?" question.
*   Identify the peak sales month (likely holiday season).
*   Identify the most valuable customer segment.
*   Suggest which product categories the business should focus on next.

---

## 🛠️ Tech Stack
- **Python 3.x**
- **Pandas**: For heavy data manipulation.
- **Plotly**: For interactive, premium-grade visualizations.
- **Streamlit**: For the executive intelligence dashboard.

---

## 📈 How to Run

### Local Execution (Manual)
1. Open your terminal in the `project-1` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the Intelligence Dashboard:
   ```bash
   python -m streamlit run app.py
   ```
4. The dashboard will automatically open in your default browser at `http://localhost:8501`.

### Data Requirements
The system expects the raw transaction data to be located at:
`project-1/raw/online_retail_real.csv`

---
*Created with Thiranex Intelligence Briefing V4.0 Stable*
