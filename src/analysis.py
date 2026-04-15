"""
Pet Store Analytics — Core Analysis Module
==========================================
Loads, cleans, and produces summary statistics for the 2020 pet store
records dataset. Import this module from the notebook or dashboard.
"""

import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# 1. Data Loading & Cleaning
# ---------------------------------------------------------------------------

def load_data(path: str = "data/pet_store_records_2020.csv") -> pd.DataFrame:
    """Load the raw CSV and return a cleaned DataFrame."""
    df = pd.read_csv(path)

    # Rename for clarity
    df.rename(columns={"VAP": "is_value_added_product"}, inplace=True)

    # Cast binary flags to bool for readability
    df["is_value_added_product"] = df["is_value_added_product"].astype(bool)
    df["re_buy"] = df["re_buy"].astype(bool)

    # Derive revenue column (price × sales units)
    df["revenue"] = df["price"] * df["sales"]

    # Ordered category for pet_size
    size_order = pd.CategoricalDtype(
        ["extra_small", "small", "medium", "large", "extra_large"], ordered=True
    )
    df["pet_size"] = df["pet_size"].astype(size_order)

    return df


# ---------------------------------------------------------------------------
# 2. Summary Statistics
# ---------------------------------------------------------------------------

def summary_stats(df: pd.DataFrame) -> dict:
    """Return a dict of high-level KPIs."""
    return {
        "total_records": len(df),
        "total_revenue": df["revenue"].sum(),
        "avg_price": df["price"].mean(),
        "avg_sales": df["sales"].mean(),
        "avg_rating": df["rating"].mean(),
        "rebuy_rate_pct": df["re_buy"].mean() * 100,
        "vap_share_pct": df["is_value_added_product"].mean() * 100,
        "unique_vendors": df["vendor_id"].nunique(),
        "unique_products": df["product_id"].nunique(),
        "countries": df["country"].nunique(),
    }


# ---------------------------------------------------------------------------
# 3. Segment-level Aggregations
# ---------------------------------------------------------------------------

def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("product_category")
        .agg(
            total_revenue=("revenue", "sum"),
            avg_price=("price", "mean"),
            total_units_sold=("sales", "sum"),
            avg_rating=("rating", "mean"),
            rebuy_rate=("re_buy", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )


def revenue_by_country(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("country")
        .agg(
            total_revenue=("revenue", "sum"),
            avg_rating=("rating", "mean"),
            num_products=("product_id", "nunique"),
            rebuy_rate=("re_buy", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )


def metrics_by_pet_type(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("pet_type")
        .agg(
            total_revenue=("revenue", "sum"),
            avg_price=("price", "mean"),
            avg_sales=("sales", "mean"),
            avg_rating=("rating", "mean"),
            rebuy_rate=("re_buy", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )


def vap_vs_standard(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("is_value_added_product")
        .agg(
            count=("product_id", "count"),
            avg_price=("price", "mean"),
            avg_sales=("sales", "mean"),
            avg_rating=("rating", "mean"),
            rebuy_rate=("re_buy", "mean"),
            avg_revenue=("revenue", "mean"),
        )
        .reset_index()
    )


def top_vendors(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("vendor_id")
        .agg(
            total_revenue=("revenue", "sum"),
            avg_rating=("rating", "mean"),
            product_count=("product_id", "nunique"),
        )
        .sort_values("total_revenue", ascending=False)
        .head(n)
        .reset_index()
    )


def sales_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot: pet_type × product_category → avg sales."""
    return df.pivot_table(
        index="pet_type",
        columns="product_category",
        values="sales",
        aggfunc="mean",
    ).round(1)


def rating_distribution(df: pd.DataFrame) -> pd.Series:
    return df["rating"].value_counts().sort_index()


def rebuy_by_rating_bucket(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rating_bucket"] = pd.cut(
        df["rating"],
        bins=[0, 3, 6, 8, 10],
        labels=["Low (1-3)", "Mid (4-6)", "Good (7-8)", "Excellent (9-10)"],
    )
    return (
        df.groupby("rating_bucket", observed=True)["re_buy"]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={"re_buy": "rebuy_rate_pct"})
    )


# ---------------------------------------------------------------------------
# 4. Simple Correlation & Feature Importance
# ---------------------------------------------------------------------------

def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = ["sales", "price", "revenue", "rating", "re_buy",
                    "is_value_added_product"]
    return df[numeric_cols].astype(float).corr().round(3)


def price_tier_analysis(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price_tier"] = pd.qcut(
        df["price"],
        q=4,
        labels=["Budget", "Economy", "Mid-range", "Premium"],
    )
    return (
        df.groupby("price_tier", observed=True)
        .agg(
            avg_sales=("sales", "mean"),
            avg_rating=("rating", "mean"),
            rebuy_rate=("re_buy", "mean"),
            count=("product_id", "count"),
        )
        .reset_index()
    )
