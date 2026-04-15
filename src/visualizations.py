"""
Pet Store Analytics — Visualizations Module
============================================
All matplotlib / seaborn charts used in the notebook.
Each function returns a (fig, ax) or fig object so callers can
save or display as needed.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

# ── Global style ──────────────────────────────────────────────────────────────
PALETTE = "viridis"
BAR_COLOR = "#4C72B0"
ACCENT_COLOR = "#DD8452"

sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "figure.dpi": 130,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})


def _fmt_currency(x, _):
    if x >= 1_000_000:
        return f"${x/1e6:.1f}M"
    if x >= 1_000:
        return f"${x/1e3:.0f}K"
    return f"${x:.0f}"


# ---------------------------------------------------------------------------
# 1. Revenue by Category (horizontal bar)
# ---------------------------------------------------------------------------
def plot_revenue_by_category(data: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette(PALETTE, len(data))
    bars = ax.barh(data["product_category"], data["total_revenue"], color=colors)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_currency))
    ax.set_xlabel("Total Revenue")
    ax.set_title("Total Revenue by Product Category", fontsize=14, fontweight="bold", pad=12)
    for bar in bars:
        w = bar.get_width()
        ax.text(w * 1.01, bar.get_y() + bar.get_height() / 2,
                _fmt_currency(w, None), va="center", fontsize=9)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 2. Revenue by Country (choropleth-style bar)
# ---------------------------------------------------------------------------
def plot_revenue_by_country(data: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = sns.color_palette("coolwarm", len(data))
    ax.bar(data["country"], data["total_revenue"], color=colors, edgecolor="white")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_currency))
    ax.set_ylabel("Total Revenue")
    ax.set_xlabel("Country")
    ax.set_title("Total Revenue by Vendor Country", fontsize=14, fontweight="bold", pad=12)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 3. Sales Heatmap — pet_type × product_category
# ---------------------------------------------------------------------------
def plot_sales_heatmap(pivot: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(14, 5))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        linewidths=0.5,
        ax=ax,
        cbar_kws={"label": "Avg Units Sold"},
    )
    ax.set_title("Average Sales by Pet Type × Product Category",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Pet Type")
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 4. Rating Distribution (bar)
# ---------------------------------------------------------------------------
def plot_rating_distribution(rating_counts: pd.Series) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.bar(rating_counts.index, rating_counts.values,
                  color=sns.color_palette("RdYlGn", len(rating_counts)),
                  edgecolor="white", width=0.7)
    ax.set_xlabel("Rating (1–10)")
    ax.set_ylabel("Number of Products")
    ax.set_title("Product Rating Distribution", fontsize=14, fontweight="bold", pad=12)
    ax.set_xticks(range(1, 11))
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1,
                str(int(h)), ha="center", fontsize=9)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 5. VAP vs Standard — grouped comparison
# ---------------------------------------------------------------------------
def plot_vap_comparison(data: pd.DataFrame) -> plt.Figure:
    data = data.copy()
    data["label"] = data["is_value_added_product"].map(
        {True: "Value-Added", False: "Standard"}
    )
    metrics = ["avg_price", "avg_sales", "avg_rating", "rebuy_rate"]
    labels  = ["Avg Price ($)", "Avg Units Sold", "Avg Rating", "Re-buy Rate"]

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for ax, metric, label in zip(axes, metrics, labels):
        sns.barplot(x="label", y=metric, data=data, hue="label",
                    palette=[BAR_COLOR, ACCENT_COLOR], ax=ax, width=0.5, legend=False)
        ax.set_title(label, fontsize=11)
        ax.set_xlabel("")
        ax.set_ylabel("")
    fig.suptitle("Value-Added Products vs Standard Products",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 6. Re-buy Rate by Rating Bucket
# ---------------------------------------------------------------------------
def plot_rebuy_by_rating(data: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(data["rating_bucket"], data["rebuy_rate_pct"],
                  color=sns.color_palette("Blues_d", len(data)), edgecolor="white")
    ax.set_ylabel("Re-buy Rate (%)")
    ax.set_xlabel("Rating Bucket")
    ax.set_title("Re-buy Rate by Rating Bucket", fontsize=14, fontweight="bold", pad=12)
    ax.set_ylim(0, 100)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1,
                f"{h:.1f}%", ha="center", fontsize=10)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 7. Price Tier Analysis
# ---------------------------------------------------------------------------
def plot_price_tier_analysis(data: pd.DataFrame) -> plt.Figure:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    palette = sns.color_palette("muted", len(data))

    for ax, (metric, title) in zip(axes, [
        ("avg_sales",  "Avg Units Sold"),
        ("avg_rating", "Avg Rating"),
        ("rebuy_rate", "Re-buy Rate"),
    ]):
        sns.barplot(x="price_tier", y=metric, data=data, hue="price_tier",
                    palette=palette, ax=ax, width=0.55, legend=False)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Price Tier")
        ax.set_ylabel("")

    fig.suptitle("Metrics Across Price Tiers (Budget → Premium)",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 8. Correlation Heatmap
# ---------------------------------------------------------------------------
def plot_correlation_heatmap(corr: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 5))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f",
        cmap="coolwarm", center=0, linewidths=0.5,
        square=True, ax=ax, vmin=-1, vmax=1,
    )
    ax.set_title("Feature Correlation Matrix", fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 9. Pet Type Revenue + Rating scatter
# ---------------------------------------------------------------------------
def plot_pet_type_bubble(data: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = sns.color_palette(PALETTE, len(data))
    for i, row in data.iterrows():
        ax.scatter(
            row["avg_rating"], row["total_revenue"],
            s=row["rebuy_rate"] * 2000,
            color=colors[i], alpha=0.8, edgecolors="white", linewidth=1.5,
            label=row["pet_type"],
        )
        ax.text(row["avg_rating"] + 0.05, row["total_revenue"],
                row["pet_type"].capitalize(), fontsize=9, va="center")
    ax.set_xlabel("Avg Rating")
    ax.set_ylabel("Total Revenue ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_currency))
    ax.set_title("Pet Type: Revenue vs Rating\n(bubble size = re-buy rate)",
                 fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    return fig
