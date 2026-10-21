import streamlit as st
import pandas as pd
import os
from utils.data_loader import get_sample_data, USER_DATA_FILE, DATA_DIR, load_data, clear_data_cache
from utils.anomaly_detection import detect_anomalies
from utils.formatting import format_inr

st.set_page_config(page_title="Upload CSV - SpendWise", page_icon="📁", layout="wide")

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
        "<hr style='border-color:rgba(255,255,255,0.18); margin:10px 0;'>",
        unsafe_allow_html=True,
    )

st.markdown(
    "<h1 style='color:#123C32; margin-bottom:4px;'>📁 Upload Expense Data (CSV)</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#71817C; font-size:15px; margin-top:0;'>"
    "Import your bank statements or custom CSV files directly into SpendWise.</p>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### 1. Download Sample CSV Template")
    st.markdown(
        "Use our pre-formatted template to format your expenses correctly before uploading."
    )
    sample_df = get_sample_data()
    csv_bytes = sample_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Sample Template (CSV)",
        data=csv_bytes,
        file_name="spendwise_template.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 2. Upload Your CSV File")
    uploaded_file = st.file_uploader(
        "Drag and drop your expense CSV file here",
        type=["csv"],
        help="CSV must contain date, description, category, and amount columns.",
    )

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

            required_cols = {"date", "description", "category", "amount"}
            if required_cols.issubset(set(up_df.columns)):
                up_df["date"] = pd.to_datetime(up_df["date"], errors="coerce")
                up_df["amount"] = pd.to_numeric(up_df["amount"], errors="coerce")
                up_df.dropna(subset=["date", "amount"], inplace=True)

                if not up_df.empty:
                    os.makedirs(DATA_DIR, exist_ok=True)
                    up_df[["date", "description", "category", "amount"]].to_csv(
                        USER_DATA_FILE, index=False
                    )
                    clear_data_cache()
                    detect_anomalies.clear()
                    st.success(
                        f"🎉 Successfully imported {len(up_df)} transactions! All dashboard metrics have been updated."
                    )
                    st.balloons()
                else:
                    st.error("No valid transaction rows found after parsing.")
            else:
                missing = required_cols - set(up_df.columns)
                st.error(f"Missing required columns: {', '.join(missing)}")
        except Exception as e:
            st.error(f"Error processing CSV file: {e}")

with col2:
    st.markdown("### 📋 Required CSV Format")
    st.markdown(
        """
        Your CSV file should have the following column structure:

        | Column | Type | Example |
        | :--- | :--- | :--- |
        | `date` | YYYY-MM-DD | `2026-03-15` |
        | `description` | Text | `Swiggy Food Order` |
        | `category` | Category | `Food`, `Transport`, `Housing`, etc. |
        | `amount` | Number | `450.00` |

        > 💡 **Note**: Alternative column names like `transaction_date`, `merchant`, `type`, and `transaction_amount` are automatically supported.
        """
    )

st.markdown("<hr style='border-color:#E5E1D8; margin:28px 0;'>", unsafe_allow_html=True)

st.markdown("### Current Active Dataset Preview")
current_df = load_data()
if not current_df.empty:
    preview_df = current_df.copy().sort_values("date", ascending=False).head(10)
    preview_df["amount_formatted"] = preview_df["amount"].apply(format_inr)
    preview_df["date_str"] = preview_df["date"].dt.strftime("%Y-%m-%d")
    st.dataframe(
        preview_df[["date_str", "description", "category", "amount_formatted"]],
        use_container_width=True,
    )
else:
    st.info("No active dataset loaded.")
