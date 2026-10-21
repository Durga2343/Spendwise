import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import IsolationForest

@st.cache_data
def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    df = df.copy()
    if "is_anomaly" in df.columns:
        df = df.drop(columns=["is_anomaly"])
        
    if len(df) < 20:
        df["is_anomaly"] = False
        return df

    expense_mask = df["amount"] > 0
    expense_df = df[expense_mask].copy()
    if len(expense_df) < 20:
        df["is_anomaly"] = False
        return df
    
    # Feature engineering: log-transformed expense amount
    X = np.log1p(expense_df["amount"].values).reshape(-1, 1)
    
    model = IsolationForest(contamination=contamination, random_state=42, n_jobs=-1)
    expense_df["anomaly_score"] = model.fit_predict(X)
    expense_df["is_anomaly"] = expense_df["anomaly_score"] == -1
    
    # Assign back safely without duplicates
    df["is_anomaly"] = False
    df.loc[expense_df.index, "is_anomaly"] = expense_df["is_anomaly"].values
    
    return df

