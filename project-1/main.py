import pandas as pd
import numpy as np
import os

class IntelligenceEngine:
    """Version 4.0: High-Precision Enterprise Analytics Engine."""
    
    def __init__(self, file_path='raw/online_retail_real.csv'):
        self.file_path = file_path
        self.df = None
        
    def load_data(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Data file not found at {self.file_path}")
        self.df = pd.read_csv(self.file_path, encoding='ISO-8859-1')
        return self.df

    def clean_data(self):
        if self.df is None: self.load_data()
        self.returns_df = self.df[self.df['InvoiceNo'].str.contains('C', na=False)].copy()
        sales_df = self.df[~self.df['InvoiceNo'].str.contains('C', na=False)].copy()
        sales_df = sales_df[(sales_df['Quantity'] > 0) & (sales_df['UnitPrice'] > 0)]
        sales_df['CustomerID'] = sales_df['CustomerID'].fillna(0)
        sales_df['InvoiceDate'] = pd.to_datetime(sales_df['InvoiceDate'])
        # Global Revenue Calculation
        sales_df['TotalSales'] = sales_df['Quantity'] * sales_df['UnitPrice']
        sales_df['YearMonth'] = sales_df['InvoiceDate'].dt.to_period('M').astype(str)
        sales_df['DayOfWeek'] = sales_df['InvoiceDate'].dt.day_name()
        sales_df['Hour'] = sales_df['InvoiceDate'].dt.hour
        self.df = sales_df
        return self.df

    def _get_target_df(self, target_df):
        return target_df if target_df is not None else self.df

    def get_summary_stats(self, target_df=None):
        df = self._get_target_df(target_df)
        return {
            "total_revenue": float(df['TotalSales'].sum()),
            "transaction_count": len(df),
            "unique_customers": df['CustomerID'].nunique()
        }

    def get_rfm_analysis(self, target_df=None):
        df = self._get_target_df(target_df)
        rfm_df = df[df['CustomerID'] != 0].copy()
        if rfm_df.empty: return pd.DataFrame()
        snapshot_date = rfm_df['InvoiceDate'].max() + pd.Timedelta(days=1)
        rfm = rfm_df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
            'InvoiceNo': 'count',
            'TotalSales': 'sum'
        }).rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'TotalSales': 'Monetary'})
        for col, name in zip(['Recency', 'Frequency', 'Monetary'], ['R', 'F', 'M']):
            try:
                if col == 'Recency': rfm[name] = pd.qcut(rfm[col], 5, labels=[5, 4, 3, 2, 1])
                else: rfm[name] = pd.qcut(rfm[col].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
            except: rfm[name] = 3
        rfm['RFM_Score'] = rfm[['R', 'F', 'M']].astype(int).sum(axis=1)
        def segment_tokens(x):
            if x >= 13: return 'Champions'
            if x >= 10: return 'Loyal'
            if x >= 7: return 'Promising'
            if x >= 5: return 'Needs Attention'
            return 'At Risk'
        rfm['Segment'] = rfm['RFM_Score'].apply(segment_tokens)
        return rfm

    def get_market_basket_analysis(self, target_df=None, top_n=30):
        df = self._get_target_df(target_df)
        top_products = df['Description'].value_counts().head(top_n).index
        basket_df = df[df['Description'].isin(top_products)]
        if basket_df.empty: return pd.DataFrame()
        basket = basket_df.groupby(['InvoiceNo', 'Description'])['Quantity'].count().unstack().fillna(0)
        basket = basket.applymap(lambda x: 1 if x > 0 else 0)
        co_matrix = basket.T.dot(basket)
        for i in range(len(co_matrix)): co_matrix.iloc[i, i] = 0
        return co_matrix

    def get_cohort_retention(self, target_df=None):
        df = self._get_target_df(target_df)
        cohort_df = df[df['CustomerID'] != 0].copy()
        if cohort_df.empty: return pd.DataFrame()
        cohort_df['CohortMonth'] = cohort_df.groupby('CustomerID')['InvoiceDate'].transform('min').dt.to_period('M')
        def get_date_int(d): return d.dt.year, d.dt.month
        c_year, c_month = get_date_int(cohort_df['CohortMonth'])
        i_year, i_month = get_date_int(cohort_df['InvoiceDate'].dt.to_period('M'))
        cohort_df['CohortIndex'] = (i_year - c_year) * 12 + (i_month - c_month) + 1
        cohort_counts = cohort_df.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].nunique().reset_index()
        retention = cohort_counts.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerID')
        retention = retention.divide(retention.iloc[:, 0], axis=0)
        retention.index = [str(i) for i in retention.index]
        retention.columns = [str(c) for c in retention.columns]
        return retention

    def get_price_elasticity(self, target_df=None):
        df = self._get_target_df(target_df).copy()
        # EXPLICIT FORCE: Ensure TotalSales is present in the results
        df['TotalSales'] = df['Quantity'] * df['UnitPrice']
        return df.groupby('Description').agg({'UnitPrice': 'mean', 'Quantity': 'sum', 'TotalSales': 'sum'})

    def get_temporal_distribution(self, target_df=None):
        df = self._get_target_df(target_df)
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return df.pivot_table(index='DayOfWeek', columns='Hour', values='InvoiceNo', aggfunc='count').reindex(day_order)

    def get_return_metrics(self, target_df=None):
        if target_df is not None:
            available = target_df['Description'].unique()
            r_df = self.returns_df[self.returns_df['Description'].isin(available)]
        else: r_df = self.returns_df
        return r_df.groupby('Description').agg({'Quantity': lambda x: abs(x.sum()), 'InvoiceNo': 'count'}).rename(columns={'Quantity': 'RefundQuantity', 'InvoiceNo': 'RefundCount'}).sort_values('RefundCount', ascending=False)

    def get_descriptive_stats(self, target_df=None):
        df = self._get_target_df(target_df)
        stats = df[['Quantity', 'UnitPrice', 'TotalSales']].describe().T
        stats = stats[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
        return stats
