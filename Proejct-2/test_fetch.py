from sklearn.datasets import fetch_openml
try:
    print("Fetching dataset 45547 from OpenML...")
    cardio = fetch_openml(data_id=45547, as_frame=True, parser='auto')
    df = cardio.frame
    print("Dataset fetched successfully!")
    print(f"Shape: {df.shape}")
    print("Columns:", df.columns.tolist())
    print(df.head())
except Exception as e:
    print(f"Error fetching from OpenML: {e}")
