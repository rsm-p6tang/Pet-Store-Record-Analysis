# 🐾 Pet Store Business Analytics 

A complete **data & business analytics** project built on a 2020 pet store supply-chain dataset covering 879 product records across 9 countries, 6 pet types, and 11 product categories.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

---

## 📊 Project Overview

| Dimension | Detail |
|-----------|--------|
| Records | 879 product records |
| Countries | 9 (India, USA, Germany, Japan, Belgium, Vietnam, Singapore, Turkey, Sri Lanka) |
| Pet Types | Dog, Cat, Fish, Bird, Rabbit, Hamster |
| Product Categories | Food, Toys, Medicine, Equipment, Snack, Supplements, Bedding, Housing, Clothes, Accessory, Grooming |
| Key Metrics Analysed | Revenue, Sales Volume, Price Tiers, Re-buy Rate, Ratings, VAP vs Standard |

---

## 🗂️ Project Structure

```
pet_store_analytics/
│
├── data/
│   └── pet_store_records_2020.csv   # Raw dataset
│
├── src/
│   ├── analysis.py                  # Data loading, cleaning & aggregations
│   └── visualizations.py            # All matplotlib/seaborn chart functions
│
├── notebooks/
│   └── pet_store_analysis.ipynb    # Full EDA & business analysis notebook
│
├── dashboard/
│   └── app.py                       # Interactive Streamlit dashboard
│
├── requirements.txt
└── README.md
```

---

## 🔑 Key Findings

1. **Revenue is concentrated** — the top 3 product categories account for the majority of total revenue.
2. **Value-Added Products (VAP)** command higher average prices while maintaining similar sales volumes, suggesting stronger margin potential.
3. **Re-buy rate is ~46.6%** — nearly half of customers repurchase, indicating moderate brand loyalty.
4. **Rating and re-buy are weakly correlated** — products rated 9–10 re-buy at ~50%+, pointing to quality as a retention lever.
5. **India dominates vendor share** (~40% of records), creating supplier concentration risk.
6. **Dog products lead revenue** across most categories; fish and hamster products present growth opportunities.
7. **Premium-priced products** don't always outsell budget items — bundling strategies may be needed.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/USERNAME/pet-store-analytics.git
cd pet-store-analytics
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Jupyter Notebook (EDA)
```bash
jupyter notebook notebooks/pet_store_analysis.ipynb
```

### 4. Launch the Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

The dashboard will open at `http://localhost:8501` with interactive filters for country, pet type, category, and product type.

---

## 📈 Dashboard Features

- **KPI Cards** — Total revenue, avg price, avg rating, re-buy rate, VAP share
- **Revenue Tab** — Category/country bar charts + pet type × category sales heatmap
- **Pet & Price Tab** — Bubble chart (revenue vs rating, sized by re-buy rate), price tier analysis, VAP comparison
- **Ratings Tab** — Rating distribution histogram + re-buy rate by rating bucket
- **Deep Dive Tab** — Correlation matrix, top vendors table, raw data explorer
- **Sidebar Filters** — Filter by country, pet type, product category, VAP status

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `pandas` | Data loading, cleaning, aggregation |
| `numpy` | Numerical operations |
| `matplotlib` + `seaborn` | Static charts & visualisations |
| `plotly` | (Available for interactive charts) |
| `streamlit` | Interactive web dashboard |
| `scikit-learn` | (Available for ML extensions) |
| `jupyter` | Exploratory analysis notebook |

---

## 📁 Dataset Column Reference

| Column | Type | Description |
|--------|------|-------------|
| `product_id` | int | Unique product identifier |
| `product_category` | str | Category (Food, Toys, Medicine, ...) |
| `sales` | int | Units sold |
| `price` | int | Unit price |
| `VAP` | bool | 1 = Value-Added Product |
| `vendor_id` | str | Vendor identifier |
| `country` | str | Vendor country |
| `pet_size` | str | Target pet size (extra_small → extra_large) |
| `pet_type` | str | Target pet (dog, cat, fish, bird, rabbit, hamster) |
| `rating` | int | Product rating (1–10) |
| `re_buy` | bool | 1 = Customer repurchased |

---

## 🔮 Possible Extensions

- [ ] **Churn / re-buy prediction** using logistic regression or a gradient boosted model
- [ ] **Price elasticity modelling** per category
- [ ] **Vendor scorecard** combining rating, rebuy rate, and revenue concentration
- [ ] **Time-series simulation** if date columns are added to the dataset
- [ ] **Deploy dashboard** on Streamlit Community Cloud

---

## 📄 License

MIT — free to use for personal and commercial projects.
