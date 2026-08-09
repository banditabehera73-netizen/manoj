from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CLEANED_DATA_PATH = Path('data/processed/sales_data_cleaned.csv')
FIGURES_DIR = Path('reports/figures')
DASHBOARD_PATH = Path('reports/dashboard.html')


def build_visualizations() -> None:
    if not CLEANED_DATA_PATH.exists():
        raise FileNotFoundError(f'Cleaned dataset not found: {CLEANED_DATA_PATH}. Run data_cleaning.py first.')

    df = pd.read_csv(CLEANED_DATA_PATH)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Basic style settings
    sns.set_theme(style='whitegrid')

    # 1. Sales by Region
    region_sales = df.groupby('region')['sales'].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=region_sales.index, y=region_sales.values, palette='viridis')
    plt.title('Total Sales by Region')
    plt.xlabel('Region')
    plt.ylabel('Sales ($)')
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'sales_by_region.png', dpi=150)
    plt.close()

    # 2. Profit by Category
    category_profit = df.groupby('product_category')['profit'].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=category_profit.index, y=category_profit.values, palette='rocket')
    plt.title('Total Profit by Product Category')
    plt.xlabel('Product Category')
    plt.ylabel('Profit ($)')
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'profit_by_category.png', dpi=150)
    plt.close()

    # 3. Customer age distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['customer_age'].dropna(), bins=10, kde=True, color='steelblue')
    plt.title('Customer Age Distribution')
    plt.xlabel('Customer Age')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'customer_age_distribution.png', dpi=150)
    plt.close()

    # 4. Sales vs Profit scatter plot
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='sales', y='profit', hue='region', alpha=0.9)
    plt.title('Sales vs Profit by Region')
    plt.xlabel('Sales ($)')
    plt.ylabel('Profit ($)')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'sales_vs_profit.png', dpi=150)
    plt.close()

    # 5. Order priority summary
    priority_counts = df['order_priority'].value_counts()
    plt.figure(figsize=(7, 5))
    sns.barplot(x=priority_counts.index, y=priority_counts.values, palette='pastel')
    plt.title('Order Priority Distribution')
    plt.xlabel('Priority')
    plt.ylabel('Orders')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'order_priority_distribution.png', dpi=150)
    plt.close()

    # Create a simple HTML dashboard
    summary = {
        'total_revenue': round(float(df['sales'].sum()), 2),
        'total_profit': round(float(df['profit'].sum()), 2),
        'avg_order_value': round(float(df['sales'].mean()), 2),
        'total_orders': int(df['order_id'].nunique()),
        'top_region': region_sales.index[0],
        'top_category': category_profit.index[0],
    }

    dashboard_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sales Data Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f6f7fb; color: #20263a; }}
    h1 {{ color: #174169; }}
    .summary {{ display: flex; gap: 20px; margin-bottom: 30px; }}
    .card {{ background: white; padding: 20px; border-radius: 12px; width: 200px; box-shadow: 0 3px 10px rgba(0,0,0,.08); }}
    .card h3 {{ margin-top: 0; color: #2a6f97; }}
    .chart-grid {{ display: grid; grid-template-columns: repeat(2, minmax(300px, 1fr)); gap: 20px; }}
    img {{ width: 100%; border-radius: 8px; background: white; padding: 5px; border: 1px solid #dce2ea; }}
  </style>
</head>
<body>
  <h1>Sales Data Cleaning & Visualization Dashboard</h1>

  <section class="summary">
    <div class="card">
      <h3>Total Revenue</h3>
      <p>${summary['total_revenue']:,.2f}</p>
    </div>
    <div class="card">
      <h3>Total Profit</h3>
      <p>${summary['total_profit']:,.2f}</p>
    </div>
    <div class="card">
      <h3>Average Order Value</h3>
      <p>${summary['avg_order_value']:,.2f}</p>
    </div>
    <div class="card">
      <h3>Total Orders</h3>
      <p>{summary['total_orders']}</p>
    </div>
  </section>

  <section class="summary">
    <div class="card">
      <h3>Top Region</h3>
      <p>{summary['top_region']}</p>
    </div>
    <div class="card">
      <h3>Top Product Category</h3>
      <p>{summary['top_category']}</p>
    </div>
  </section>

  <section class="chart-grid">
    <img src="figures/sales_by_region.png" alt="Sales by Region">
    <img src="figures/profit_by_category.png" alt="Profit by Category">
    <img src="figures/customer_age_distribution.png" alt="Customer Age Distribution">
    <img src="figures/sales_vs_profit.png" alt="Sales vs Profit">
  </section>
</body>
</html>
"""

    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD_PATH.write_text(dashboard_html, encoding='utf-8')

    print('Visualization dashboard created successfully.')


if __name__ == '__main__':
    build_visualizations()
    print('Generated plots in reports/figures')
