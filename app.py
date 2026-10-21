import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_data, get_sample_data, clear_data_cache
from utils.analytics import (
    calculate_metrics, plot_expense_by_category,
    plot_monthly_trend, CATEGORY_COLORS, PALETTE,
    FOREST_GREEN, EMERALD_GREEN, CHART_LAYOUT,
)
from utils.anomaly_detection import detect_anomalies

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpendWise — Smart Expense Analyzer",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.auth import check_login
check_login()

# ── Load CSS (Cached for speed) ───────────────────────────────────────────────
@st.cache_data
def get_css(file_name):
    try:
        with open(file_name) as f:
            return f"<style>{f.read()}</style>"
    except FileNotFoundError:
        return ""

st.markdown(get_css("assets/styles.css"), unsafe_allow_html=True)

# ── Sidebar branding ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='color:#FFFFFF; margin-bottom:2px;'>💸 SpendWise</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#A8C3AE; margin-top:0; font-size:13px;'>"
        "Track · Analyze · Save</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<hr style='border-color:rgba(255,255,255,0.12); margin:10px 0;'>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>" * 4, unsafe_allow_html=True)
    st.markdown(
        "<p style='color:rgba(255,255,255,0.50); font-size:12px; font-style:italic;'>"
        "Better choices today,<br>bigger dreams tomorrow.</p>",
        unsafe_allow_html=True,
    )

# ── Page header ───────────────────────────────────────────────────────────────
username = st.session_state.get("username", "there")
st.markdown(
    f"<h1 style='color:#123C32; margin-bottom:4px;'>Good morning, {username.capitalize()}! 👋</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#71817C; font-size:16px; margin-top:0;'>"
    "Here's what's happening with your expenses today.</p>",
    unsafe_allow_html=True,
)

# ── Load & process data ───────────────────────────────────────────────────────
df = load_data()
if df.empty:
    st.warning("No data found. Please upload your expenses or use sample data.")
    st.stop()

df = detect_anomalies(df)

# ── Metrics row ───────────────────────────────────────────────────────────────
total_spend, avg_daily, highest_cat, highest_cat_pct, anomaly_count = calculate_metrics(df)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Expenses", f"₹{total_spend:,.2f}", delta="−2% vs last month", delta_color="inverse")
with col2:
    st.metric("Average Daily Spend", f"₹{avg_daily:,.2f}")
with col3:
    st.metric("Top Category", highest_cat, f"{highest_cat_pct:.1f}% of total")
with col4:
    st.metric("Unusual Alerts", anomaly_count, "Flagged by ML", delta_color="off")

st.markdown(
    "<hr style='border-color:#E5E1D8; margin:24px 0;'>",
    unsafe_allow_html=True,
)

# ── Main analytics row ────────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### Expense by Category")
    fig_cat = plot_expense_by_category(df)
    st.plotly_chart(fig_cat, use_container_width=True)

with col_b:
    st.markdown("### Monthly Spending Trend")
    fig_trend = plot_monthly_trend(df)
    st.plotly_chart(fig_trend, use_container_width=True)

with col_c:
    st.markdown("### Recent Transactions")
    recent_df = df.sort_values(by="date", ascending=False).head(5)
    for _, row in recent_df.iterrows():
        dot_color = "#E9A0AA" if row.get("is_anomaly", False) else "#10A878"
        status_emoji = "⚠️" if row.get("is_anomaly", False) else "✔️"
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; align-items:center;"
            f"padding:10px 14px; margin-bottom:8px; background:#FFFFFF; border-radius:10px;"
            f"border:1px solid #E5E1D8; box-shadow:0 2px 8px rgba(18,60,50,0.04);'>"
            f"<div>"
            f"<p style='margin:0; font-weight:600; color:#183B35; font-size:14px;'>"
            f"{row['description']}</p>"
            f"<p style='margin:0; color:#71817C; font-size:12px;'>{row['category']} · "
            f"{row['date'].strftime('%d %b %Y')}</p>"
            f"</div>"
            f"<div style='text-align:right;'>"
            f"<p style='margin:0; font-weight:700; color:#123C32; font-size:14px;'>"
            f"₹{row['amount']:,.2f}</p>"
            f"<span style='font-size:11px; color:{dot_color};'>{status_emoji}</span>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

st.markdown(
    "<hr style='border-color:#E5E1D8; margin:24px 0;'>",
    unsafe_allow_html=True,
)

# ── Secondary dashboard row ───────────────────────────────────────────────────
st.markdown(
    "<h3 style='color:#123C32;'>Secondary Dashboard</h3>",
    unsafe_allow_html=True,
)
col_d, col_e = st.columns([2, 1])

with col_d:
    st.markdown("#### Spending By Day")
    expense_df = df[df["amount"] > 0]
    daily = expense_df.groupby(expense_df["date"].dt.date)["amount"].sum().reset_index()
    if not daily.empty:
        fig_bar = go.Figure(go.Bar(
            x=daily["date"],
            y=daily["amount"],
            marker_color=EMERALD_GREEN,
            marker_line_color="#FFFFFF",
            marker_line_width=0.5,
            hovertemplate="<b>%{x}</b><br>₹%{y:,.2f}<extra></extra>",
            name="Daily Spend",
        ))
        fig_bar.update_layout(
            **CHART_LAYOUT,
            bargap=0.3,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No daily expense data available.")

with col_e:
    st.markdown("#### Upload Expense Data")
    st.markdown(
        "<p style='color:#71817C; font-size:13px; margin-top:-8px;'>"
        "Drag and drop your CSV file here:</p>",
        unsafe_allow_html=True,
    )
    from utils.data_loader import USER_DATA_FILE, DATA_DIR
    import os

    sample_df = get_sample_data()
    csv = sample_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download Sample CSV", csv, "sample_expenses.csv", "text/csv")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            up_df = pd.read_csv(uploaded_file)
            up_df.columns = up_df.columns.str.lower().str.strip()
            up_df.rename(
                columns={
                    "transaction_date": "date",
                    "merchant": "description",
                    "type": "category",
                    "transaction_amount": "amount",
                },
                inplace=True,
            )
            if {"date", "description", "category", "amount"}.issubset(up_df.columns):
                up_df["date"] = pd.to_datetime(up_df["date"], errors="coerce")
                up_df["amount"] = pd.to_numeric(up_df["amount"], errors="coerce")
                up_df.dropna(subset=["date", "amount"], inplace=True)
                if not up_df.empty:
                    os.makedirs(DATA_DIR, exist_ok=True)
                    up_df.to_csv(USER_DATA_FILE, index=False)
                    clear_data_cache()
                    detect_anomalies.clear()
                    st.success("✅ File uploaded successfully!")
                    st.rerun()
                else:
                    st.error("No valid rows found after parsing.")
            else:
                st.error("Missing required columns: date, description, category, amount")
        except Exception as e:
            st.error(f"Upload error: {e}")
