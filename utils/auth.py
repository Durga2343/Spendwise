import streamlit as st
import json
import os
from utils.data_loader import DATA_DIR

USERS_FILE = os.path.join(DATA_DIR, "users.json")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {"admin": "admin"} 

def save_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)
    return True

def logout():
    st.session_state["logged_in"] = False
    st.session_state.pop("username", None)
    st.rerun()

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:

        # ── Inline styles scoped to login page ──────────────────────────────
        st.markdown("""
        <style>
        :root {
            --forest-green:   #123C32;
            --warm-cream:     #F7F5EF;
            --emerald-green:  #10A878;
            --emerald-dark:   #0D8A62;
            --sage-green:     #A8C3AE;
            --soft-lavender:  #B8A1E3;
            --dusty-rose:     #E9A0AA;
            --white:          #FFFFFF;
            --text-primary:   #183B35;
            --text-secondary: #71817C;
            --border-color:   #E5E1D8;
            --input-bg:       #F7F9F8;
        }

        .stApp {
            background-color: var(--warm-cream) !important;
            background-image:
                radial-gradient(circle at 8% 12%, rgba(168,195,174,0.30) 0%, transparent 42%),
                radial-gradient(circle at 90% 85%, rgba(184,161,227,0.12) 0%, transparent 38%),
                radial-gradient(circle at 55% 50%, rgba(233,160,170,0.06) 0%, transparent 30%);
        }

        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background-color: rgba(16, 168, 120, 0.10);
            border: 1px solid rgba(16, 168, 120, 0.25);
            color: #10A878;
            font-size: 13px;
            font-weight: 600;
            padding: 5px 14px;
            border-radius: 20px;
            margin-bottom: 18px;
        }
        .hero-title {
            font-size: 3.2rem;
            font-weight: 800;
            color: #123C32;
            line-height: 1.12;
            margin: 0 0 16px 0;
        }
        .hero-title em {
            color: #10A878;
            font-style: normal;
        }
        .hero-sub {
            color: #183B35;
            opacity: 0.75;
            font-size: 1.1rem;
            margin-bottom: 32px;
            line-height: 1.6;
        }

        .feature-item {
            display: flex;
            align-items: flex-start;
            gap: 14px;
            margin-bottom: 22px;
        }
        .feature-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }
        .fi-emerald { background-color: rgba(16,168,120,0.12); }
        .fi-lavender { background-color: rgba(184,161,227,0.18); }
        .fi-rose    { background-color: rgba(233,160,170,0.15); }
        .feature-item h5 {
            margin: 0 0 3px 0;
            font-size: 15px;
            font-weight: 600;
            color: #123C32;
        }
        .feature-item p {
            margin: 0;
            font-size: 13px;
            color: #71817C;
            line-height: 1.45;
        }

        .accent-pill {
            display: inline-block;
            background-color: rgba(168, 195, 174, 0.25);
            border: 1px solid rgba(168, 195, 174, 0.50);
            color: #123C32;
            font-size: 12px;
            padding: 4px 12px;
            border-radius: 20px;
            margin-top: 8px;
        }

        .auth-card {
            background-color: #FFFFFF;
            padding: 40px 38px;
            border-radius: 20px;
            box-shadow: 0 16px 56px rgba(18, 60, 50, 0.13);
            border: 1px solid #E5E1D8;
            position: relative;
            overflow: hidden;
        }
        .auth-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #10A878 0%, #A8C3AE 60%, #B8A1E3 100%);
        }
        .auth-card-title {
            text-align: center;
            font-size: 1.7rem;
            font-weight: 700;
            color: #123C32;
            margin: 0 0 4px 0;
        }
        .auth-card-sub {
            text-align: center;
            color: #71817C;
            font-size: 14px;
            margin-bottom: 24px;
        }

        .stTabs [data-baseweb="tab-list"] {
            background-color: #F7F9F8 !important;
            border-radius: 10px !important;
            padding: 4px !important;
            border-bottom: none !important;
            gap: 0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 8px 18px !important;
            font-weight: 500 !important;
            color: #71817C !important;
            background-color: transparent !important;
            border: none !important;
            transition: all 0.2s ease !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF !important;
            color: #10A878 !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(18,60,50,0.08) !important;
            border: none !important;
        }

        .stButton > button {
            background-color: #10A878 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            box-shadow: 0 4px 14px rgba(16,168,120,0.30) !important;
            transition: all 0.25s ease !important;
            margin-top: 6px;
        }
        .stButton > button:hover {
            background-color: #0D8A62 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(16,168,120,0.35) !important;
        }

        .stTextInput > div > div > input {
            border-radius: 10px !important;
            border: 1.5px solid #E5E1D8 !important;
            background-color: #F7F9F8 !important;
            color: #183B35 !important;
            padding: 12px 14px !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #10A878 !important;
            box-shadow: 0 0 0 2px rgba(16,168,120,0.18) !important;
        }

        .or-divider {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 14px 0;
        }
        .or-divider hr {
            flex: 1;
            border: none;
            border-top: 1px solid #E5E1D8;
            margin: 0;
        }
        .or-divider span {
            color: #71817C;
            font-size: 13px;
            font-weight: 500;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col_gap, col2 = st.columns([1.25, 0.1, 1])

        with col1:
            st.markdown("""
            <div class="hero-badge">🌱 Smart Expense Analyzer</div>
            <h1 class="hero-title">Take Control of<br><em>Your Spending</em></h1>
            <p class="hero-sub">
                Track your expenses, uncover hidden patterns, and make smarter
                financial decisions — all in one beautiful dashboard.
            </p>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="feature-item">
                <div class="feature-icon fi-emerald">📊</div>
                <div>
                    <h5>Visualize Your Spending</h5>
                    <p>Beautiful charts show exactly where your money goes, month by month.</p>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-icon fi-lavender">🧠</div>
                <div>
                    <h5>ML Anomaly Detection</h5>
                    <p>Isolation Forest automatically flags unusual transactions before they become problems.</p>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-icon fi-rose">🛡️</div>
                <div>
                    <h5>Privacy First</h5>
                    <p>All analysis happens locally — your financial data never leaves your device.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <span class="accent-pill">✦ No ads · No tracking · 100% local</span>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            st.markdown('<p class="auth-card-title">Welcome Back 👋</p>', unsafe_allow_html=True)
            st.markdown('<p class="auth-card-sub">Log in or create your SpendWise account</p>', unsafe_allow_html=True)

            tab_login, tab_signup = st.tabs(["  Log In  ", "  Sign Up  "])

            with tab_login:
                st.markdown("<br>", unsafe_allow_html=True)
                username = st.text_input("Email / Username", key="login_user", placeholder="e.g. admin")
                password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")

                c1, c2 = st.columns(2)
                with c1:
                    st.checkbox("Remember me", key="remember_me")
                with c2:
                    st.markdown(
                        "<p style='text-align:right; color:#10A878; font-size:13px; "
                        "margin-top:10px; cursor:pointer;'>Forgot password?</p>",
                        unsafe_allow_html=True
                    )

                if st.button("➔  Log In", use_container_width=True, key="btn_login"):
                    users = load_users()
                    if username in users and users[username] == password:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.rerun()
                    else:
                        st.error("Incorrect username or password. Please try again.")

                st.markdown("""
                <div class="or-divider">
                    <hr><span>OR</span><hr>
                </div>
                """, unsafe_allow_html=True)

                if st.button("G  Continue with Google", use_container_width=True, key="btn_google"):
                    st.info("Google OAuth is not configured yet. Please use username/password login.")

            with tab_signup:
                st.markdown("<br>", unsafe_allow_html=True)
                new_username = st.text_input("Choose Username", key="reg_user", placeholder="e.g. jane_doe")
                new_password = st.text_input("Choose Password", type="password", key="reg_pass", placeholder="Min 6 characters")
                confirm_pw   = st.text_input("Confirm Password", type="password", key="reg_conf", placeholder="Re-enter password")

                if st.button("Create Account", use_container_width=True, key="btn_signup"):
                    if new_password != confirm_pw:
                        st.error("Passwords do not match!")
                    elif new_username and new_password:
                        if save_user(new_username, new_password):
                            st.success("🎉 Account created! Switch to Log In tab to continue.")
                        else:
                            st.error("Username already taken. Please choose another.")
                    else:
                        st.error("Please fill out all fields.")

                st.markdown("""
                <p style='text-align:center; font-size:12px; color:#71817C; margin-top:14px;'>
                    By signing up, your data stays 100% on your device.
                </p>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.stop()

    # ── Render Logged-In User Badge & Log Out Button in Sidebar (on all pages) ─────────────
    with st.sidebar:
        st.markdown(
            "<hr style='border-color:rgba(255,255,255,0.18); margin:20px 0 12px 0;'>",
            unsafe_allow_html=True,
        )
        username = st.session_state.get("username", "User")
        initial = username[0].upper() if username else "U"
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:10px; margin-bottom:12px; "
            f"padding:8px 10px; background:rgba(255,255,255,0.06); border-radius:10px;'>"
            f"<div style='width:34px; height:34px; border-radius:50%; background:#10A878; "
            f"display:flex; align-items:center; justify-content:center; color:#FFFFFF; font-weight:700; font-size:15px;'>"
            f"{initial}</div>"
            f"<div style='flex:1; min-width:0;'>"
            f"<p style='margin:0; font-size:10px; color:rgba(255,255,255,0.65); text-transform:uppercase; letter-spacing:0.5px;'>Logged in as</p>"
            f"<p style='margin:0; font-weight:700; color:#FFFFFF; font-size:14px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;'>{username.capitalize()}</p>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        if st.button("🚪 Log Out", key="sidebar_logout_button", use_container_width=True):
            logout()
