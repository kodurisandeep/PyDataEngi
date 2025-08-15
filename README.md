# 🚀 PyDataEngi: Practical Data Engineering & EDA in Python

**PyDataEngi** is a hands-on repository that explores real-world techniques in data engineering, cleaning, transformation, and exploratory data analysis — all built with Python and designed for modular execution. Each script is self-contained, parameterized where needed, and focused on reproducibility, auditability, and clarity.

---

## 🔍 Topics Covered

### 📁 File Formats & Conversion
- Read/write support for CSV, TSV, Excel, JSON, XML, Parquet, ZIP, and GZIP
- Encoding handling, delimiter parsing, and multi-sheet Excel ingestion
- Format conversion utilities: JSON ⇄ CSV, Excel ⇄ CSV

### 🧼 Data Cleaning & Validation
- Missing value handling: `dropna`, `fillna`, null logic
- Duplicate detection and removal
- Regex-based text cleaning and normalization
- Date/time parsing, timezone conversion
- Column renaming, reordering, and type inference
- Outlier detection via boxplots, Z-score, and IQR
- Schema validation using Pydantic and manual rules

### 📊 Exploratory Data Analysis (EDA)
- Descriptive statistics: `describe()`, quantiles, distributions
- Grouping and aggregation: `groupby`, `pivot_table`
- Categorical analysis: frequency counts, scheme mapping
- Time-series resampling and rolling averages
- Visualizations using matplotlib and seaborn:
  - Line plots, histograms, KDE overlays
  - Correlation heatmaps and dashboard-style layouts

### 🧪 Feature Engineering & ETL Design
- Derived columns: ratios, flags, transformations
- Encoding techniques: one-hot, label encoding, mapping
- Configurable ETL scripts using `argparse` and YAML
- Compressed output formats: `.zip`, `.gzip`, `.parquet`
- Structured logging via `python-json-logger`
- Graceful error handling and recovery logic

### ☁️ GCP-Ready Production Pipelines
- Read/write operations with GCS using `gcsfs` and `fsspec`
- IAM role validation and secure access patterns
- Secrets management via Secret Manager
- BigQuery ingestion using `pandas_gbq` and `google-cloud-bigquery`
- Structured logging and failed record capture to GCS/BigQuery
- Alert simulation via Pub/Sub and Cloud Monitoring
- Modular orchestration using Prefect flows

---

## ✨ Philosophy

Curated by [@kodurisandeep](https://github.com/kodurisandeep), PyDataEngi emphasizes:
- Deep understanding over “just works” solutions
- Secure, teardown-safe automation
- Transparent logging and actionable monitoring
- Reusable patterns for real-world data workflows
- Documentation-first mindset for onboarding and sharing

Explore the full repository at [PyDataEngi on GitHub](https://github.com/kodurisandeep/PyDataEngi) to dive into the scripts and see each module in action.
