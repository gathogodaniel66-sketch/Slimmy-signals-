import streamlit as st
import pandas as pd
import random
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

# ---------------- STYLING ---------------- #

st.markdown("""

<style>

.stApp{
background-color:#0B1220;
color:white;
}

section[data-testid="stSidebar"]{
background:#111827;
}

.card{
background:#151D2E;
padding:20px;
border-radius:15px;
border:1px solid #28344F;
margin:5px;
}

.signal-card{
background:#151D2E;
padding:25px;
border-radius:18px;
border:1px solid #2E3A59;
}

h1,h2,h3{
color:white;
}

</style>

""", unsafe_allow_html=True)

# ---------------- STORAGE ---------------- #

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📊 SLIMMY SIGNALS")

page = st.sidebar.radio(

"Navigation",

[
"Dashboard",
"Signals",
"Analytics",
"History",
"Settings"

]

)

st.sidebar.write("Status: 🟢 LIVE")

# ---------------- HEADER ---------------- #

st.title(APP_NAME)

st.caption(
"Professional Multi-Market Trading Dashboard"
)

# ---------------- TOP METRICS ---------------- #

m1,m2,m3,m4 = st.columns(4)

with m1:
    st.metric(
        "Markets",
        len(MARKETS)
    )

with m2:
    st.metric(
        "Signals",
        len(st.session_state.history)
    )

with m3:
    st.metric(
        "Confidence",
        f"{random.randint(78,96)}%"
    )

with m4:
    st.metric(
        "System",
        "ONLINE"
    )

st.divider()

# ---------------- MARKET AREA ---------------- #

left,middle,right = st.columns([2,1,1])

with left:

    st.subheader(
        "Market Performance"
    )

    chart_data = pd.DataFrame({

        "Price":[

            100,
            103,
            105,
            101,
            108,
            111,
            115,
            118

        ]

    })

    st.line_chart(
        chart_data
    )

with middle:

    st.subheader(
        "Watchlist"
    )

    watch = st.multiselect(

        "",

        MARKETS,

        default=[

            "EUR/USD",
            "XAU/USD"

        ]

    )

    st.write(watch)

with right:

    st.subheader(
        "Sessions"
    )

    st.success(
        "London Open"
    )

    st.info(
        "New York Active"
    )

    st.warning(
        "Asia Waiting"
    )

st.divider()

# ---------------- SIGNAL AREA ---------------- #

c1,c2 = st.columns(2)

with c1:

    market = st.selectbox(

        "Choose Market",

        MARKETS

    )

with c2:

    timeframe = st.selectbox(

        "Timeframe",

        [

            "M5",
            "M15",
            "H1",
            "H4"

        ]

    )

if st.button(

    "Generate Professional Signal"

):

    signal = generate_signal()

    st.markdown(

    f"""

    <div class='signal-card'>

    <h2>{signal['signal']}</h2>

    <h3>Confidence: {signal['confidence']}%</h3>

    <p>Market: {market}</p>

    <p>Timeframe: {timeframe}</p>

    <p>Take Profit: {signal['tp']}</p>

    <p>Stop Loss: {signal['sl']}</p>

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

# ---------------- ANALYTICS ---------------- #

if page == "Analytics":

    st.subheader(
        "Performance Analytics"
    )

    if len(
        st.session_state.history
    ) > 0:

        df = pd.DataFrame(

            st.session_state.history

        )

        st.bar_chart(

            df["confidence"]

        )

# ---------------- HISTORY ---------------- #

if page == "History":

    st.subheader(
        "Signal History"
    )

    st.dataframe(

        pd.DataFrame(

            st.session_state.history

        )

    )

# ---------------- SETTINGS ---------------- #

if page == "Settings":

    st.subheader(
        "Settings"
    )

    st.toggle(
        "Enable Alerts"
    )

    st.toggle(
        "Dark Mode"
    )

# ---------------- NOTES ---------------- #

st.divider()

st.text_area(

    "Trading Journal"

)
