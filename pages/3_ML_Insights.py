import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.anomaly_detection import detect_anomalies
from utils.formatting import format_inr
from utils.analytics import CHART_LAYOUT, FOREST_GREEN, EMERALD_GREEN, DUSTY_ROSE, SAGE_GREEN

st.set_page_config(page_title="ML Insights - SpendWise", page_icon="🤖", layout="wide")

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
    "<h1 style='color:#123C32; margin-bottom:4px;'>🤖 Machine Learning Insights</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    """<p style='color:#71817C; font-size:15px; margin-top:0;'>
    We use an <b style='color:#123C32;'>Isolation Forest</b> model to detect unusual spending patterns.
    <em>Note: Unusual does not necessarily mean fraudulent.</em></p>""",
    unsafe_allow_html=True,
)

df = load_data()
if df.empty:
    st.info("No data available.")
    st.stop()

df = detect_anomalies(df)

total_tx     = len(df)
anomalies    = df[df["is_anomaly"] == True]
anomaly_count = len(anomalies)

if total_tx < 20:
    st.warning(
        "Not enough data to train a meaningful anomaly detector. "
        "Need at least 20 transactions. Keep adding data!"
    )
    st.stop()

# ── Metrics ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions",  total_tx)
col2.metric("Flagged as Unusual",  anomaly_count, "Needs Review", delta_color="inverse")
col3.metric("Anomaly Percentage", f"{(anomaly_count / total_tx) * 100:.1f}%")

st.markdown(
    "<hr style='border-color:#E5E1D8; margin:24px 0;'>",
    unsafe_allow_html=True,
)

# ── Charts ────────────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### Amount Distribution — Ordinary vs Unusual")
    plot_df = df.copy()
    plot_df["Anomaly Status"] = plot_df["is_anomaly"].map({True: "Unusual", False: "Ordinary"})

    ordinary = plot_df[plot_df["Anomaly Status"] == "Ordinary"]["amount"]
    unusual  = plot_df[plot_df["Anomaly Status"] == "Unusual"]["amount"]

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=ordinary,
        name="Ordinary",
        marker_color=EMERALD_GREEN,
        opacity=0.80,
        nbinsx=50,
        hovertemplate="Amount: ₹%{x:,.2f}<br>Count: %{y}<extra>Ordinary</extra>",
    ))
    fig.add_trace(go.Histogram(
        x=unusual,
        name="Unusual",
        marker_color=DUSTY_ROSE,
        opacity=0.85,
        nbinsx=50,
        hovertemplate="Amount: ₹%{x:,.2f}<br>Count: %{y}<extra>Unusual</extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        barmode="overlay",
        legend=dict(font=dict(color=FOREST_GREEN), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.markdown("### Flagged Transactions")
    if anomaly_count > 0:
        display_anom = anomalies.copy()
        display_anom["Amount"] = display_anom["amount"].apply(format_inr)
        display_anom["Date"]   = display_anom["date"].dt.strftime("%d %b %Y")

        # Styled anomaly cards
        for _, row in display_anom.iterrows():
            st.markdown(
                f"""
                <div class="anomaly-card">
                  <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                      <p style='margin:0; font-weight:700; color:#123C32; font-size:14px;'>
                        ⚠️ {row['description']}</p>
                      <p style='margin:2px 0 0 0; color:#71817C; font-size:12px;'>
                        {row['category']} · {row['Date']}</p>
                    </div>
                    <p style='margin:0; font-weight:700; color:#E9A0AA; font-size:15px;'>
                      {row['Amount']}</p>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div style='background:rgba(16,168,120,0.08); border:1px solid rgba(16,168,120,0.20);
            border-left:4px solid #10A878; border-radius:12px; padding:20px 24px; text-align:center;'>
              <p style='margin:0; font-size:16px; font-weight:600; color:#123C32;'>
                ✅ No unusual transactions detected!</p>
              <p style='margin:6px 0 0 0; color:#71817C; font-size:13px;'>
                Your spending looks consistent and within normal patterns.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Explainer ─────────────────────────────────────────────────────────────────
st.markdown(
    "<hr style='border-color:#E5E1D8; margin:24px 0;'>",
    unsafe_allow_html=True,
)
with st.expander("🔍 How does Isolation Forest work?"):
    st.markdown("""
    **Isolation Forest** is an unsupervised machine learning algorithm that identifies anomalies
    by randomly isolating observations.

    - It selects a random feature and a random split value between the min and max of that feature.
    - Anomalies are **"few and different"** — they require fewer splits to isolate.
    - Transactions that are isolated in fewer steps receive a higher anomaly score.
    - We flag the top **5%** of transactions by anomaly score as *Unusual*.

    > ⚠️ **Important distinction:** An *unusual* transaction means it deviates from your typical
    > spending pattern — it is **not** automatically fraudulent. Review flagged items in context.
    """)

import os
pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SpendWise_Complete_Viva_Guide.pdf")
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📄 Download Complete Viva & Project Defense Guide (PDF)",
        data=pdf_bytes,
        file_name="SpendWise_Complete_Viva_Guide.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

