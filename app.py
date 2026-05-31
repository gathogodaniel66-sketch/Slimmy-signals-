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

st.markdown("""

<style>

.main{
background-color:#0E1117;
color:white;
}

.metric-box{
padding:20px;
border-radius:12px;
background:#1E1E1E;
text-align:center;
margin:5px;
}

.signal-card{
padding:20px;
border-radius:15px;
background:#161B22;
border:1px solid #30363D;
}

</style>

""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history=[]

st.sidebar.title("📊 SLIMMY SIGNALS")

page = st.sidebar.radio(

"Menu",

[
"Dashboard",
"History",
"Analytics"
]

)

st.title(APP_NAME)

st.caption(
"Professional Multi Market Trading Dashboard"
)

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Markets",
        len(MARKETS)
    )

with c2:
    st.metric(
        "Signals",
        len(st.session_state.history)
    )

with c3:
    st.metric(
        "Status",
        "LIVE"
    )

with c4:
    st.metric(
        "Users",
        "VIP"
    )

st.divider()

left,right = st.columns([2,1])

with left:

    market = st.selectbox(
        "Select Market",
        MARKETS
    )

    timeframe = st.selectbox(

        "Timeframe",

        ["M5","M15","H1","H4"]

    )

    if st.button(
        "Generate Signal"
    ):

        signal = generate_signal()

        st.markdown(

        f"""

        <div class="signal-card">

        <h2>{signal["signal"]}</h2>

        <h3>Confidence: {signal["confidence"]}%</h3>

        <p>TP: {signal["tp"]}</p>

        <p>SL: {signal["sl"]}</p>

        <p>Market: {market}</p>

        </div>

        """,

        unsafe_allow_html=True

        )

        st.session_state.history.append({

            "time":datetime.now(),

            "market":market,

            "signal":signal["signal"],

            "confidence":signal["confidence"]

        })

with right:

    st.subheader(
        "Watchlist"
    )

    watch = st.multiselect(

        "",

        MARKETS,

        default=["EUR/USD","XAU/USD"]

    )

    st.write(watch)

if page=="History":

    st.subheader(
        "Signal History"
    )

    st.dataframe(

        pd.DataFrame(

            st.session_state.history

        )

    )

if page=="Analytics":

    st.subheader(
        "Analytics"
    )

    st.bar_chart(

        pd.DataFrame(

            st.session_state.history

        )["confidence"]

        if len(st.session_state.history)>0

        else []

    )

st.divider()

st.text_area(

"Trading Notes"

)
