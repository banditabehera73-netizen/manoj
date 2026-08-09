from pathlib import Path
import json

import numpy as np
import pandas as pd

RAW_DATA_PATH = Path('data/raw/sales_data_raw.csv')
PROCESSED_DIR = Path('data/processed')
PROCESSED_PATH = PROCESSED_DIR / 'sales_data_cleaned.csv'
REPORT_PATH = Path('reports')
QUALITY_REPORT_PATH = REPORT_PATH / 'data_quality_summary.json'


def clean_data() -> pd.DataFrame:
    """Load, clean, and save the raw sales dataset."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f'Missing raw dataset: {RAW_DATA_PATH}')

    df = pd.read_csv(RAW_DATA_PATH)

    initial_shape = df.shape

    # Step 1: Remove exact duplicate rows based on order_id and other row-level duplicates
    df = df.drop_duplicates()

    # Step 2: Normalize business columns
    df.columns = [col.strip().lower() for col in df.columns]

    # Step 3: Convert dates and numeric columns
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    numeric_cols = ['customer_age', 'sales', 'quantity', 'discount', 'profit']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Step 4: Standardize categorical values
    df['segment'] = df['segment'].astype(str).str.title().replace({'Home Office': 'Home Office'})
    df['region'] = df['region'].astype(str).str.title()
    df['state'] = df['state'].astype(str).str.upper()
    df['product_category'] = df['product_category'].fillna('Uncategorized').astype(str).str.title()
    df['product_name'] = df['product_name'].fillna('Unknown Product').astype(str).str.title()
    df['order_priority'] = df['order_priority'].fillna('Medium').astype(str).str.title()

    # Step 5: Handle missing values
    df['customer_age'] = df['customer_age'].fillna(df['customer_age'].median())
    df['segment'] = df['segment'].replace('Nan', pd.NA).replace('nan', pd.NA)
    df['segment'] = df['segment'].fillna('Consumer')

    df['sales'] = df['sales'].fillna(df['sales'].median())
    df['quantity'] = df['quantity'].fillna(df['quantity'].median())
    df['discount'] = df['discount'].fillna(df['discount'].median())
    df['profit'] = df['profit'].fillna(df['profit'].median())

    # Step 6: Remove impossible or invalid records
    df = df[df['sales'] >= 0]
    df = df[df['quantity'] >= 0]
    df = df[df['profit'] >= -1000]

    # Step 7: Outlier handling for numeric columns using IQR logic
    def cap_outliers(series: pd.Series) -> pd.Series:
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return series.clip(lower=lower, upper=upper)

    for col in ['sales', 'quantity', 'profit', 'discount']:
        df[col] = cap_outliers(df[col])

    # Step 8: Round numeric values for readability
    df['sales'] = df['sales'].round(2)
    df['profit'] = df['profit'].round(2)
    df['discount'] = df['discount'].round(2)

    # customer_age should be integer
    df['customer_age'] = df['customer_age'].round().astype('Int64')

    # Step 9: Create derived features for insurance quality analysis
    df['profit_margin'] = (df['profit'] / df['sales']).replace([np.inf, -np.inf], np.nan).fillna(0)

    # Save cleaned file
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_PATH, index=False)

    # Quality report
    quality_report = {
        'source_rows': int(initial_shape[0]),
        'rows_after_deduplication': int(df.shape[0] + (initial_shape[0] - df.shape[0])),
        'rows_after_cleaning': int(df.shape[0]),
        'missing_values_before': int(df.isna().sum().sum()),
        'missing_values_after': int(df.isna().sum().sum()),
        'duplicates_removed': int(initial_shape[0] - df.shape[0]),
        'columns': list(df.columns),
        'date_range': {
            'start': df['order_date'].min().date().isoformat() if 'order_date' in df.columns and not df['order_date'].isna().all() else None,
            'end': df['order_date'].max().date().isoformat() if 'order_date' in df.columns and not df['order_date'].isna().all() else None,
        },
    }

    with QUALITY_REPORT_PATH.open('w', encoding='utf-8') as f:
        json.dump(quality_report, f, indent=2)

    return df


if __name__ == '__main__':
    cleaned_df = clean_data()
    print(f'Cleaned data saved to {PROCESSED_PATH}')
    print(f'Rows: {len(cleaned_df)}')
