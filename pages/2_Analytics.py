import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.analytics import (
    plot_expense_by_category, plot_monthly_trend,
    CATEGORY_COLORS, PALETTE, CHART_LAYOUT,
    FOREST_GREEN, EMERALD_GREEN, SAGE_GREEN,
)
from utils.formatting import format_inr

st.set_page_config(page_title="Analytics - SpendWise", page_icon="📈", layout="wide")

from utils.auth import check_login
check_login()

@st.cache_data
def get_css(file_name):
    try:
        with open(file_name) as f:
            return f"<style>{f.read()}</style>"
    except FileNotFoundError:
        return ""

st.markdown(get_css("assets/styles.css"), unsafe_allow_html=True)

# Sidebar branding
with st.sidebar:
    st.markdown(
        "<h2 style='color:#FFFFFF; margin-bottom:2px;'>💸 SpendWise</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#A8C3AE; margin-top:0; font-size:13px;'>Track · Analyze · Save</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<hr style='border-color:rgba(255,255,255,0.12); margin:10px 0;'>",
        unsafe_allow_html=True,
    )


st.markdown(
    "<h1 style='color:#123C32; margin-bottom:4px;'>📈 Deep Dive Analytics</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#71817C; font-size:15px; margin-top:0;'>"
    "Explore your spending patterns across time and categories.</p>",
    unsafe_allow_html=True,
)

df = load_data()
if df.empty:
    st.info("No data available for analytics.")
    st.stop()

expense_df = df[df["amount"] > 0].copy()
if expense_df.empty:
    st.warning("No expense data (amount > 0) available to analyze.")
    st.stop()

# ── Row 1: Donut + Monthly Trend ──────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Expense Distribution")
    st.plotly_chart(plot_expense_by_category(df), use_container_width=True)

with col2:
    st.markdown("### Monthly Trend")
    st.plotly_chart(plot_monthly_trend(df), use_container_width=True)

# ── Row 2: Daily bar + Avg by Category bar ───────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("### Daily Spending")
    daily = expense_df.groupby(expense_df["date"].dt.date)["amount"].sum().reset_index()
    fig_bar = go.Figure(go.Bar(
        x=daily["date"],
        y=daily["amount"],
        marker_color=EMERALD_GREEN,
        marker_line_color="#FFFFFF",
        marker_line_width=0.5,
        hovertemplate="<b>%{x}</b><br>₹%{y:,.2f}<extra></extra>",
        name="Daily Spend",
    ))
    fig_bar.update_layout(**CHART_LAYOUT, bargap=0.3)
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.markdown("### Average Spend by Category")
    avg_cat = expense_df.groupby("category")["amount"].mean().reset_index()
    avg_cat = avg_cat.sort_values("amount", ascending=False)
    colors = [CATEGORY_COLORS.get(c, PALETTE[i % len(PALETTE)]) for i, c in enumerate(avg_cat["category"])]

    fig_avg = go.Figure(go.Bar(
        x=avg_cat["category"],
        y=avg_cat["amount"],
        marker_color=colors,
        marker_line_color="#FFFFFF",
        marker_line_width=0.5,
        hovertemplate="<b>%{x}</b><br>Avg: ₹%{y:,.2f}<extra></extra>",
        name="Avg Spend",
    ))
    fig_avg.update_layout(**CHART_LAYOUT, bargap=0.35)
    st.plotly_chart(fig_avg, use_container_width=True)

# ── AI Insight card ───────────────────────────────────────────────────────────
st.markdown(
    "<hr style='border-color:#E5E1D8; margin:24px 0;'>",
    unsafe_allow_html=True,
)
highest_cat = expense_df.groupby("category")["amount"].sum().idxmax()
highest_pct = (
    expense_df.groupby("category")["amount"].sum().max()
    / expense_df["amount"].sum()
) * 100

st.markdown(
    f"""
    <div style='background:linear-gradient(135deg,rgba(16,168,120,0.08),rgba(168,195,174,0.10));
    border:1px solid rgba(16,168,120,0.18); border-left:4px solid #10A878;
    border-radius:12px; padding:20px 24px; margin-top:8px;'>
      <p style='margin:0 0 4px 0; color:#71817C; font-size:12px; font-weight:600;
      text-transform:uppercase; letter-spacing:0.6px;'>💡 AI-Generated Insight</p>
      <p style='margin:0; color:#123C32; font-size:16px; font-weight:500; line-height:1.55;'>
        <b>{highest_cat}</b> accounts for <b>{highest_pct:.1f}%</b> of your total spending.
        Consider reviewing these expenses if you'd like to save more this month.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)
