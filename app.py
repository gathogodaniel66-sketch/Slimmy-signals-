import streamlit as st
from scanner import generate_signal
from auth import login
from config import APP_NAME, MARKETS

st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)

login()

st.title(APP_NAME)

st.subheader(
    "Professional Trading Dashboard"
)

market = st.selectbox(
    "Choose Market",
    MARKETS
)

if st.button(
    "Generate Signal"
):

    result = generate_signal()

    st.metric(
        "Signal",
        result["signal"]
    )

    st.metric(
        "Confidence %",
        result["confidence"]
    )

    st.metric(
        "Take Profit",
        result["tp"]
    )

    st.metric(
        "Stop Loss",
        result["sl"]
    )

st.divider()

st.subheader(
    "Trading Notes"
)

notes = st.text_area(
    "Write notes here"
)

st.sidebar.title(
    "Slimmy Signals"
)

st.sidebar.success(
    "Cloud Bot Running"
)
