"""
Pet Store Analytics — Interactive Streamlit Dashboard
======================================================
Run with:  streamlit run dashboard/app.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

from src.analysis import (
    load_data, summary_stats, revenue_by_category, revenue_by_country,
    metrics_by_pet_type, vap_vs_standard, top_vendors, sales_heatmap_data,
    rating_distribution, rebuy_by_rating_bucket, correlation_matrix,
    price_tier_analysis,
)
from src.visualizations import (
    plot_revenue_by_category, plot_revenue_by_country, plot_sales_heatmap,
    plot_rating_distribution, plot_vap_comparison, plot_rebuy_by_rating,
    plot_price_tier_analysis, plot_correlation_heatmap, plot_pet_type_bubble,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pet Store Analytics 2020",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load & cache data ──────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'pet_store_records_2020.csv')

@st.cache_data
def get_data():
    return load_data(DATA_PATH)

df_full = get_data()

# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.title("🐾 Filters")

all_countries = sorted(df_full["country"].unique())
sel_countries = st.sidebar.multiselect("Country", all_countries, default=all_countries)

all_pet_types = sorted(df_full["pet_type"].unique())
sel_pets = st.sidebar.multiselect("Pet Type", all_pet_types, default=all_pet_types)

all_categories = sorted(df_full["product_category"].unique())
sel_cats = st.sidebar.multiselect("Product Category", all_categories, default=all_categories)

vap_choice = st.sidebar.radio("Product Type", ["All", "Value-Added Only", "Standard Only"])

# Apply filters
df = df_full.copy()
df = df[df["country"].isin(sel_countries)]
df = df[df["pet_type"].isin(sel_pets)]
df = df[df["product_category"].isin(sel_cats)]
if vap_choice == "Value-Added Only":
    df = df[df["is_value_added_product"]]
elif vap_choice == "Standard Only":
    df = df[~df["is_value_added_product"]]

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🐾 Pet Store Business Analytics — 2020")
st.markdown(f"Showing **{len(df):,}** of **{len(df_full):,}** records  |  Use the sidebar to filter.")
st.divider()

# ── KPI cards ──────────────────────────────────────────────────────────────────
kpis = summary_stats(df)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue",    f"${kpis['total_revenue']:,.0f}")
k2.metric("Avg Unit Price",   f"${kpis['avg_price']:,.0f}")
k3.metric("Avg Rating",       f"{kpis['avg_rating']:.2f} / 10")
k4.metric("Re-buy Rate",      f"{kpis['rebuy_rate_pct']:.1f}%")
k5.metric("VAP Share",        f"{kpis['vap_share_pct']:.1f}%")
st.divider()

# ── Revenue tab ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📦 Revenue", "🐶 Pet & Price", "⭐ Ratings", "🔬 Deep Dive"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Category")
        fig = plot_revenue_by_category(revenue_by_category(df))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with col2:
        st.subheader("Revenue by Country")
        fig = plot_revenue_by_country(revenue_by_country(df))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.subheader("Sales Heatmap — Pet Type × Category")
    fig = plot_sales_heatmap(sales_heatmap_data(df))
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pet Type: Revenue, Rating & Re-buy")
        fig = plot_pet_type_bubble(metrics_by_pet_type(df))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with col2:
        st.subheader("Price Tier Analysis")
        fig = plot_price_tier_analysis(price_tier_analysis(df))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.subheader("Value-Added vs Standard Products")
    fig = plot_vap_comparison(vap_vs_standard(df))
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Rating Distribution")
        fig = plot_rating_distribution(rating_distribution(df))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with col2:
        st.subheader("Re-buy Rate by Rating Bucket")
        fig = plot_rebuy_by_rating(rebuy_by_rating_bucket(df))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Feature Correlation Matrix")
        fig = plot_correlation_heatmap(correlation_matrix(df))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with col2:
        st.subheader("Top 10 Vendors by Revenue")
        vendors = top_vendors(df, n=10)
        st.dataframe(
            vendors.style.format({"total_revenue": "${:,.0f}", "avg_rating": "{:.2f}"}),
            use_container_width=True,
        )

    st.subheader("Raw Data Explorer")
    st.dataframe(df, use_container_width=True, height=300)

st.divider()
st.caption("Pet Store Analytics 2020 — Built with Python, pandas, matplotlib, seaborn & Streamlit")
