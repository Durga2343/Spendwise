import streamlit as st
import pandas as pd
from utils.data_loader import load_data, clear_data_cache, USER_DATA_FILE
from utils.formatting import format_inr
from utils.anomaly_detection import detect_anomalies
import os

st.set_page_config(page_title="Transactions - SpendWise", page_icon="📝", layout="wide")

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

st.markdown(
    "<h1 style='color:#123C32; margin-bottom:4px;'>📝 Transaction History</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#71817C; font-size:15px; margin-top:0;'>"
    "Browse, filter, and manage all your expense records.</p>",
    unsafe_allow_html=True,
)

df = load_data()
df = detect_anomalies(df)

if df.empty:
    st.info("No transactions found. Go to 'Upload Data' to add your expenses.")
    st.stop()

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
    st.markdown("### Filters")
    search_term = st.text_input("Search description")
    categories = st.multiselect("Category", options=df['category'].unique())

    min_date, max_date = df['date'].min(), df['date'].max()
    date_range = st.date_input("Date Range", [min_date, max_date])

# Apply filters
filtered_df = df.copy()
if search_term:
    filtered_df = filtered_df[filtered_df['description'].str.contains(search_term, case=False, na=False)]
if categories:
    filtered_df = filtered_df[filtered_df['category'].isin(categories)]
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

st.markdown(f"**Showing {len(filtered_df)} transactions**")

# Display table
display_df = filtered_df.copy()
display_df['amount_formatted'] = display_df['amount'].apply(format_inr)
display_df['date_str'] = display_df['date'].dt.strftime('%Y-%m-%d')
display_df['Anomaly Status'] = display_df['is_anomaly'].map({True: '⚠️ Unusual', False: '✔️ Normal'})

st.dataframe(display_df[['date_str', 'description', 'category', 'amount_formatted', 'Anomaly Status']], use_container_width=True)

# Add Transaction Form
st.markdown("### Add Manual Transaction")
with st.form("add_transaction"):
    col1, col2, col3, col4 = st.columns(4)
    new_date = col1.date_input("Date")
    new_desc = col2.text_input("Description")
    new_cat = col3.selectbox("Category", ["Food", "Transport", "Housing", "Utilities", "Entertainment", "Shopping", "Health", "Other"])
    new_amount = col4.number_input("Amount (₹)", min_value=0.0, step=10.0)
    
    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        if new_desc and new_amount > 0:
            new_row = pd.DataFrame([{
                "date": pd.to_datetime(new_date),
                "description": new_desc,
                "category": new_cat,
                "amount": new_amount
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            # Save to user data
            os.makedirs("data", exist_ok=True)
            updated_df[['date', 'description', 'category', 'amount']].to_csv(USER_DATA_FILE, index=False)
            clear_data_cache()
            detect_anomalies.clear()
            st.success("Transaction added successfully! Refreshing...")
            st.rerun()
        else:
            st.error("Please provide a valid description and amount.")
