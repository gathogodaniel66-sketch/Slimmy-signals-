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

# ---------------- STYLE ---------------- #

st.markdown("""

<style>

.stApp{
background:#0B1220;
color:white;
}

section[data-testid="stSidebar"]{
background:#111827;
}

.block{
background:#151D2E;
padding:20px;
border-radius:18px;
border:1px solid #26344F;
margin-bottom:15px;
}

.bigblock{
background:#151D2E;
padding:25px;
border-radius:18px;
border:1px solid #26344F;
min-height:420px;
}

.smallblock{
background:#151D2E;
padding:18px;
border-radius:18px;
border:1px solid #26344F;
min-height:180px;
}

.signal{
background:#1A2335;
padding:25px;
border-radius:18px;
border:1px solid #344766;
}

</style>

""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history=[]

st.sidebar.title("📊 KIHATOS SIGNALS")

page = st.sidebar.radio(

"Navigation",

[
"Dashboard",
"History",
"Analytics",
"Settings"

]

)

# -------- TOP KPIs -------- #

k1,k2,k3,k4 = st.columns(4)

k1.metric(
"Markets",
len(MARKETS)
)

k2.metric(
"Signals",
len(st.session_state.history)
)

k3.metric(
"Accuracy",
f"{random.randint(78,96)}%"
)

k4.metric(
"Status",
"LIVE"
)

st.divider()

# =================================
# TRUE BENTO GRID
# =================================

left,right = st.columns([3,1])

# BIG PANEL

with left:

    st.markdown(
    "### Market Overview"
    )

    prices = pd.DataFrame({

    "Price":[

    100,
    102,
    105,
    104,
    108,
    112,
    115,
    118,
    117,
    121

    ]

    })

    st.line_chart(
    prices
    )

# STACKED RIGHT CARDS

with right:

    st.markdown(
    "### Watchlist"
    )

    watch = st.multiselect(

    "",

    MARKETS,

    default=[

    "EUR/USD",

    "XAU/USD"

    ]

    )

    st.markdown(
    "### Sessions"
    )

    st.success(
    "London"
    )

    st.info(
    "New York"
    )

    st.warning(
    "Asia"
    )

st.divider()

# SECOND BENTO ROW

r1,r2,r3 = st.columns([2,1,1])

with r1:

    market = st.selectbox(

    "Market",

    MARKETS

    )

    timeframe = st.selectbox(

    "Timeframe",

    [

    "M5",
    "M15",
    "H1",
    "H4"

    ]

    )

with r2:

    st.metric(

    "Confidence",

    f"{random.randint(70,95)}%"

    )

with r3:

    st.metric(

    "Trend",

    random.choice(

    [

    "BUY",

    "SELL",

    "NEUTRAL"

    ]

    )

    )

st.divider()

# LARGE SIGNAL PANEL

st.subheader(
"Signal Center"
)

if st.button(
"Generate Signal"
):

    signal = generate_signal()

    st.markdown(

    f"""

    <div class='signal'>

    <h2>{signal["signal"]}</h2>

    <h3>Confidence: {signal["confidence"]}%</h3>

    <p>Market: {market}</p>

    <p>Timeframe: {timeframe}</p>

    <p>TP: {signal["tp"]}</p>

    <p>SL: {signal["sl"]}</p>

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

# LOWER BENTO

bottom_left,bottom_right = st.columns([2,1])

with bottom_left:

    st.subheader(
    "History"
    )

    st.dataframe(

    pd.DataFrame(

    st.session_state.history

    )

    )

with bottom_right:

    st.subheader(
    "Analytics"
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

st.text_area(

"Trading Journal",

height=150

)
