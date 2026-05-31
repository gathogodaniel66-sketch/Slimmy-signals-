import streamlit as st
import pandas as pd
from datetime import datetime

from scanner import generate_signal
from auth import login
from config import APP_NAME, MARKETS

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📈",
    layout="wide"
)

login()

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.title("SLIMMY SIGNALS")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Analytics",
        "History"
    ]
)

watchlist = st.sidebar.multiselect(
    "Watchlist",
    MARKETS,
    default=["EUR/USD","XAU/USD"]
)

st.title("📈 " + APP_NAME)

col1,col2,col3 = st.columns(3)

col1.metric(
    "Markets",
    len(MARKETS)
)

col2.metric(
    "Watchlist",
    len(watchlist)
)

col3.metric(
    "Signals Today",
    len(st.session_state.history)
)

market = st.selectbox(
    "Market",
    MARKETS
)

timeframe = st.selectbox(
    "Timeframe",
    ["M5","M15","H1","H4"]
)

if st.button("Generate Professional Signal"):

    result = generate_signal()

    confidence_color = "🟢"

    if result["confidence"] < 60:
        confidence_color = "🟡"

    if result["confidence"] < 57:
        confidence_color = "🔴"

    st.success(
        f"{result['signal']} | {confidence_color} {result['confidence']}%"
    )

    signal_data = {

        "time": datetime.now().strftime("%H:%M"),

        "market": market,

        "timeframe": timeframe,

        "signal": result["signal"],

        "confidence": result["confidence"],

        "tp": result["tp"],

        "sl": result["sl"]

    }

    st.session_state.history.append(
        signal_data
    )

if menu == "History":

    st.subheader(
        "Signal History"
    )

    st.dataframe(
        pd.DataFrame(
            st.session_state.history
        )
    )

elif menu == "Analytics":

    st.subheader(
        "Analytics"
    )

    st.write(
        "Signals generated:",
        len(st.session_state.history)
    )

st.divider()

st.subheader(
    "Trading Notes"
)

st.text_area(
    "Write notes"
)

st.sidebar.success(
    "Cloud Bot Running"
)
