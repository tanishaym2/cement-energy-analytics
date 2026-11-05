# 🏭 Industrial Production & Energy Analytics Dashboard

An end-to-end industrial analytics platform built to analyze production, energy consumption, transportation, material composition, and environmental impact for Indian cement manufacturing plants.

The project processes Life Cycle Inventory (LCI) data, stores it in a structured database, performs analytics, and visualizes key business insights through an interactive Streamlit dashboard.

---

## 📌 Project Overview

This project was developed as part of an industrial internship to transform raw cement production data into actionable insights.

The system follows a complete Data Engineering and Analytics pipeline:

Raw Dataset
→ ETL Pipeline
→ Data Cleaning
→ SQLite Database
→ KPI Generation
→ Analytics Engine
→ Business Insights
→ Interactive Dashboard

---

## ✨ Features

- Automated ETL pipeline
- SQLite database integration
- Industrial KPI generation
- Plant performance analytics
- Energy consumption analysis
- CO₂ emissions analysis
- Material composition analysis
- Transport analysis
- Executive dashboard
- Business insights generation
- AI-style recommendations
- Interactive Streamlit dashboard

---

## 🏗️ System Architecture

```
Raw Excel Dataset
        │
        ▼
 ETL Pipeline
 (Parsing & Cleaning)
        │
        ▼
 Normalized CSV Files
        │
        ▼
 SQLite Database
        │
        ▼
 Analytics Engine
        │
        ▼
 KPI Generation
        │
        ▼
 Exported Reports
        │
        ▼
 Streamlit Dashboard
```

---

# 📂 Project Structure

```
cement-energy-analytics
│
├── dashboard/
│   ├── app.py
│   ├── charts.py
│   └── utils.py
│
├── data/
│   ├── interim/
│   ├── processed/
│   └── exports/
│
├── src/
│   ├── analytics/
│   ├── database/
│   ├── etl/
│   ├── exports/
│   ├── ml/
│   └── utils/
│
├── notebooks/
├── sql/
├── tests/
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 📊 Dashboard Modules

## Executive Dashboard

- Plant KPIs
- Product Summary
- Material Summary
- Transport Statistics
- Emission Statistics

---

## Plant Performance

- Material Quantity
- Plant Benchmarking
- Performance Comparison

---

## Energy Analytics

- Energy Consumption
- Energy Distribution
- Plant-wise Energy Usage

---

## CO₂ Analytics

- CO₂ Emissions
- Environmental Impact
- Sustainability Metrics

---

## Transport Analytics

- Average Distance
- Maximum Distance
- Transportation Records

---

## Material Composition

- OPC
- PPC
- PSC
- Raw Material Distribution

---

## AI Business Insights

- Operational Insights
- Recommendations
- Performance Summary

---

# 📈 Analytics Generated

✔ Plant Performance

✔ Transport Analysis

✔ Energy Analysis

✔ CO₂ Analysis

✔ Composition Analysis

✔ Executive Dashboard

✔ Business Recommendations

✔ KPI Reports

---

# 🛠️ Tech Stack

### Programming

- Python

### Data Analysis

- Pandas
- NumPy

### Database

- SQLite

### Visualization

- Streamlit
- Plotly

### Version Control

- Git
- GitHub

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/bhakti263/cement-energy-analytics.git
```

Move into the project

```bash
cd cement-energy-analytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the dashboard

```bash
streamlit run dashboard/app.py
```

---

# 📸 Dashboard Preview

Add screenshots here.

Example:

```
dashboard/images/dashboard.png
```

---

# 🚀 Future Enhancements

- Predictive energy consumption using Machine Learning
- Carbon footprint forecasting
- Interactive geographical transport maps
- Real-time IoT integration
- Plant anomaly detection
- Automated report generation
- Dashboard deployment on Streamlit Cloud

---

# 📚 Dataset

The project is based on industrial cement production and Life Cycle Inventory (LCI) datasets used for production, energy, transportation, and sustainability analysis.

---
