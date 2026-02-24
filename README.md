# 🏠 HDB Resale Flat Prices ETL Pipeline

## 📌 Overview
This project implements a **production-style ETL pipeline** to process HDB resale flat prices data from **January 2012 to December 2016**, sourced from data.gov.sg.

The pipeline is designed to be:
- Modular  
- Config-driven  
- Idempotent  
- Scalable  

---

## ⚙️ Tech Stack
- Python (Pandas, Requests)  
- YAML (Configuration)  
- Jupyter Notebook (Demonstration)  
- VS Code (Development)  

---

## 📁 Project Structure

```bash
hdb_etl/
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   ├── combined/
│   ├── cleaned/
│   ├── transformed/
│   ├── hashed/
│   └── failed/
├── notebooks/
│   └── HDB_ETL_Jupyter.ipynb
├── src/
│   ├── extract.py
│   ├── combine.py
│   ├── validation.py
│   ├── cleaning.py
│   ├── transformation.py
│   ├── hashing.py
│   ├── anomaly.py
│   └── utils.py
├── main.py
└── README.md
🔄 Pipeline Flow
Raw → Combined → Validated → Cleaned → Transformed → Hashed → Anomalies
🚀 How to Run
1. Install dependencies
pip install pandas requests pyyaml matplotlib
2. Run full pipeline
python main.py
3. Run via Notebook

Open:

notebooks/HDB_ETL_Jupyter.ipynb

Execute cells sequentially.

📥 Data Extraction

API-based ingestion from data.gov.sg

No manual download required

Includes retry & polling for large datasets

🧹 Data Quality & Cleaning
Validation Rules

Valid date format

Valid storey range (e.g., "01 TO 03")

Non-null critical fields

Cleaning Steps

Standardization (uppercase categorical fields)

Duplicate removal using composite key

Retain highest resale price

🧮 Transformation Logic
Resale Identifier Format
S + Block(3 digits) + Price Prefix + Month + Town Initial
Example
S1232301A
🔐 Hashing

Algorithm: SHA-256

Ensures:

Irreversibility

Uniqueness

Data privacy

📊 Anomaly Detection

Method: Interquartile Range (IQR)

Identifies outliers in resale price

📦 Outputs
Output Type	Description
Raw	Original data
Cleaned	Validated & deduplicated
Transformed	With Resale Identifier
Hashed	With hashed identifier
Failed	Invalid + anomaly records
🧠 Engineering Design

Config-driven via YAML

Modular pipeline (separation of concerns)

Idempotent execution (skip logic)

Logging-enabled for traceability

📌 Assumptions

HDB lease duration is 99 years

Composite key excludes resale price

Dataset schema is consistent across files

📈 Insights

Majority of resale prices fall within expected IQR range

Minimal anomalies detected, indicating high data quality

Strong consistency across towns and flat types

📬 Submission Notes

Fully automated pipeline (no manual intervention)

Notebook included for step-by-step execution

Designed with production best practices