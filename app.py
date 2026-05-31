import streamlit as st
from scanner import generate_signal
from auth import login
from config import APP_NAME, MARKETS

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📈",
    layout="wide"
)

login()

st.title("📈 " + APP_NAME)

st.markdown(
"""
### AI Powered Trading Dashboard
Multi-market scanner • Risk tools • Analytics
"""
)

col1, col2 = st.columns(2)

with col1:

    market = st.selectbox(
        "Select Market",
        MARKETS
    )

with col2:

    timeframe = st.selectbox(
        "Timeframe",
        ["M5","M15","H1","H4"]
    )

if st.button("Generate Signal"):

    result = generate_signal()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "SIGNAL",
        result["signal"]
    )

    c2.metric(
        "CONFIDENCE",
        str(result["confidence"])+"%"
    )

    c3.metric(
        "TP",
        result["tp"]
    )

    c4.metric(
        "SL",
        result["sl"]
    )

st.divider()

st.subheader("Risk Calculator")

balance = st.number_input(
    "Account Balance",
    value=100
)

risk = st.slider(
    "Risk %",
    1,
    10,
    2
)

risk_amount = balance * (risk/100)

st.success(
    f"Risk Amount: {risk_amount}"
)

st.divider()

st.subheader(
    "Trading Notes"
)

st.text_area(
    "Write notes here"
)

st.sidebar.title(
    "Slimmy Signals"
)

st.sidebar.success(
    "Cloud Bot Active"
)

st.sidebar.write(
"""
Version 1.0
Professional Edition
"""
)
