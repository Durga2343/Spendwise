import streamlit as st
import os
from utils.data_loader import USER_DATA_FILE, DATA_FILE, save_sample_data, clear_data_cache
from utils.anomaly_detection import detect_anomalies
from utils.auth import check_login, logout

st.set_page_config(page_title="Settings - SpendWise", page_icon="⚙️", layout="wide")

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
        "<p style='color:#A8C3AE; margin-top:0; font-size:13px;'>Smart Expense Analyzer</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='margin-top:5px; margin-bottom:15px; border-color:rgba(255,255,255,0.18);'>", unsafe_allow_html=True)

st.markdown(
    "<h1 style='color:#123C32; margin-bottom:4px;'>⚙️ Settings & Documentation</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#71817C; font-size:15px; margin-top:0;'>"
    "Manage your data, account session, application preferences, and viva documentation.</p>",
    unsafe_allow_html=True,
)

# ── Session & Account ────────────────────────────────────────────────────────
st.markdown("### 👤 Account & Session")
username = st.session_state.get("username", "User")
col_user, col_logout = st.columns([3, 1])
with col_user:
    st.markdown(
        f"<p style='font-size:15px; color:#183B35;'>Currently logged in as: <b style='color:#10A878;'>{username.capitalize()}</b></p>",
        unsafe_allow_html=True,
    )
with col_logout:
    if st.button("🚪 Log Out Now", key="settings_logout_btn", use_container_width=True):
        logout()

st.markdown("---")

# ── Project Viva Guide PDF Download ──────────────────────────────────────────
st.markdown("### 🎓 Project & Viva Preparation Guide")
st.markdown(
    "<p style='color:#71817C; font-size:14px; margin-top:0;'>"
    "Download the comprehensive project documentation and viva defense guide containing architecture details, "
    "ML Isolation Forest mathematical training explanations, feature engineering, and 30+ viva Q&As.</p>",
    unsafe_allow_html=True,
)

pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SpendWise_Complete_Viva_Guide.pdf")
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="📄 Download Complete Viva Guide (PDF)",
        data=pdf_bytes,
        file_name="SpendWise_Complete_Viva_Guide.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
else:
    st.info("Viva Guide PDF is being compiled or not found at root.")

st.markdown("---")

# ── Data Management ──────────────────────────────────────────────────────────
st.markdown("### 📊 Data Management")

if st.button("Reset Sample Data"):
    save_sample_data()
    clear_data_cache()
    detect_anomalies.clear()
    st.success("Sample data has been regenerated.")
    st.rerun()

st.markdown("---")
st.markdown("### ⚠️ Clear User Data")
st.warning("This will permanently delete any uploaded or manually entered transactions.")

confirm = st.checkbox("I understand this action cannot be undone.")
if st.button("Delete My Data", type="primary", disabled=not confirm):
    if os.path.exists(USER_DATA_FILE):
        os.remove(USER_DATA_FILE)
        clear_data_cache()
        detect_anomalies.clear()
        st.success("User data successfully deleted. The app will now use sample data.")
        st.rerun()
    else:
        st.info("No user data found to delete.")

st.markdown("---")
st.markdown("### 🛡️ About SpendWise")
st.info("SpendWise is a local, privacy-first personal expense analyzer. None of your data is sent to external servers or APIs.")

