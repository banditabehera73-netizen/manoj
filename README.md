# Data Cleaning & Visualization Project

This project demonstrates a complete internship-style data analysis workflow using a raw sales dataset.

## Project Goal

The goal is to clean raw business data, prepare it for analysis, detect key business patterns, and create visual insights that can be presented in a dashboard or report.

## Key Features

- Handle missing values, duplicates, inconsistent categorical values, incorrect numeric data, and outliers
- Use Python libraries such as Pandas, Matplotlib, and Seaborn
- Generate cleaned data files and business-friendly visualizations
- Create a simple HTML dashboard summarizing key findings

## Project Structure

- `data/raw/`: raw source dataset
- `data/processed/`: cleaned dataset
- `src/`: Python scripts for data cleaning and visualization
- `reports/figures/`: generated chart images
- `reports/`: business insights and dashboard files

## Dataset

The project uses a synthetic sales dataset representing online retail orders. The raw dataset intentionally includes duplicates, missing values, inconsistent values, and outliers to mimic real-world data quality issues.

## Installation

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python src/data_cleaning.py
python src/visualize.py
```

## Expected Outcome

By the end of the project, you will have:

- A clean, usable dataset
- A repeatable preprocessing workflow
- Insightful charts and visual representations
- A dashboard/report ready for stakeholder presentation
