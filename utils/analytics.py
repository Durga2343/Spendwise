import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ── Official Palette ──────────────────────────────────────────────────────────
FOREST_GREEN   = "#123C32"
EMERALD_GREEN  = "#10A878"
SAGE_GREEN     = "#A8C3AE"
SOFT_LAVENDER  = "#B8A1E3"
DUSTY_ROSE     = "#E9A0AA"
WARM_CREAM     = "#F7F5EF"
TEXT_SECONDARY = "#71817C"

# ── Consistent Category → Color Mapping (used on ALL pages) ──────────────────
CATEGORY_COLORS = {
    "Food":          EMERALD_GREEN,
    "Transport":     SAGE_GREEN,
    "Shopping":      SOFT_LAVENDER,
    "Bills":         DUSTY_ROSE,
    "Housing":       "#5A8C7A",   # mid-tone forest-to-emerald
    "Utilities":     "#7BBDAA",   # lighter emerald
    "Entertainment": "#C9B8F0",   # lighter lavender
    "Health":        "#D4EDE6",   # very light emerald
    "Other":         FOREST_GREEN,
}

# Fallback ordered palette for categories not explicitly listed
PALETTE = [EMERALD_GREEN, SAGE_GREEN, SOFT_LAVENDER, DUSTY_ROSE,
           "#5A8C7A", "#7BBDAA", "#C9B8F0", FOREST_GREEN]

# ── Shared chart layout defaults ──────────────────────────────────────────────
CHART_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color=FOREST_GREEN, family="Inter, Segoe UI, sans-serif"),
    margin=dict(l=0, r=0, t=30, b=0),
    xaxis=dict(
        gridcolor="rgba(229,225,216,0.6)",
        linecolor="rgba(229,225,216,0.6)",
    ),
    yaxis=dict(
        gridcolor="rgba(229,225,216,0.6)",
        linecolor="rgba(229,225,216,0.6)",
    ),
)


def calculate_metrics(df):
    expense_df = df[df["amount"] > 0]
    total_spend = expense_df["amount"].sum()
    days = (expense_df["date"].max() - expense_df["date"].min()).days
    avg_daily = total_spend / days if days > 0 else total_spend

    if not expense_df.empty:
        cat_sums = expense_df.groupby("category")["amount"].sum()
        highest_cat = cat_sums.idxmax()
        highest_cat_pct = (cat_sums.max() / total_spend) * 100
    else:
        highest_cat = "N/A"
        highest_cat_pct = 0.0

    anomaly_count = int(df["is_anomaly"].sum()) if "is_anomaly" in df.columns else 0

    return total_spend, avg_daily, highest_cat, highest_cat_pct, anomaly_count


def _get_color_sequence(categories):
    """Return a list of colors aligned to a list of category names."""
    return [CATEGORY_COLORS.get(c, PALETTE[i % len(PALETTE)]) for i, c in enumerate(categories)]


def plot_expense_by_category(df):
    expense_df = df[df["amount"] > 0].copy()
    cat_totals = expense_df.groupby("category")["amount"].sum().reset_index()
    cat_totals = cat_totals.sort_values("amount", ascending=False)

    colors = _get_color_sequence(cat_totals["category"].tolist())

    fig = go.Figure(go.Pie(
        labels=cat_totals["category"],
        values=cat_totals["amount"],
        hole=0.52,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textfont=dict(color=FOREST_GREEN, size=12),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        showlegend=True,
        legend=dict(
            orientation="v",
            font=dict(color=FOREST_GREEN, size=12),
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    return fig


def plot_monthly_trend(df):
    expense_df = df[df["amount"] > 0].copy()
    expense_df["month"] = expense_df["date"].dt.to_period("M").dt.to_timestamp()
    monthly = expense_df.groupby("month")["amount"].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["month"],
        y=monthly["amount"],
        mode="lines+markers",
        line=dict(color=EMERALD_GREEN, width=2.5, shape="spline"),
        marker=dict(color=EMERALD_GREEN, size=7, line=dict(color="#FFFFFF", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(16,168,120,0.10)",
        hovertemplate="<b>%{x|%b %Y}</b><br>₹%{y:,.2f}<extra></extra>",
        name="Monthly Spend",
    ))
    fig.update_layout(**CHART_LAYOUT)
    return fig
