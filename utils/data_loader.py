import pandas as pd
import streamlit as st
import os

# Create absolute paths to ensure data saves and loads from the exact same directory regardless of which page is active
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "sample_expenses.csv")
USER_DATA_FILE = os.path.join(DATA_DIR, "user_expenses.csv")

def get_sample_data():
    data = {
        "date": pd.date_range(start="2023-01-01", periods=100, freq="D"),
        "description": ["Groceries", "Uber", "Rent", "Restaurant", "Salary"] * 20,
        "category": ["Food", "Transport", "Housing", "Food", "Income"] * 20,
        "amount": [1500, 300, 25000, 1200, -50000] * 20
    }
    df = pd.DataFrame(data)
    # Adding some anomalies
    df.loc[10, "amount"] = 8000
    df.loc[45, "amount"] = 12000
    return df

def save_sample_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    df = get_sample_data()
    df.to_csv(DATA_FILE, index=False)

@st.cache_data
def load_data():
    if os.path.exists(USER_DATA_FILE):
        df = pd.read_csv(USER_DATA_FILE)
    elif os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        save_sample_data()
        df = pd.read_csv(DATA_FILE)
    
    df['date'] = pd.to_datetime(df['date'])
    return df

def clear_data_cache():
    load_data.clear()
