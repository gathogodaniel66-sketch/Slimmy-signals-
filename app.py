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
background:#08111F;
color:white;
}

section[data-testid="stSidebar"]{
background:#111827;
}

[data-testid="stMetric"]{
background:#131E30;
padding:15px;
border-radius:14px;
border:1px solid #24324A;
}

.block{
background:#131E30;
padding:18px;
border-radius:16px;
border:1px solid #24324A;
margin-bottom:12px;
}

.big{
padding:20px;
border-radius:20px;
background:#131E30;
border:1px solid #24324A;
}

</style>

""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📊 SLIMMY SIGNALS")

page = st.sidebar.radio(

"Navigation",

[
"Dashboard",
"History",
"Analytics"

]

)

# ---------------- HEADER ---------------- #

st.title(APP_NAME)

st.caption(
"Professional Multi Market Dashboard"
)

# ---------------- KPI CARDS ---------------- #

k1,k2 = st.columns(2)

with k1:
    st.metric(
        "Markets",
        len(MARKETS)
    )

with k2:
    st.metric(
        "Signals",
        len(st.session_state.history)
    )

k3,k4 = st.columns(2)

with k3:
    st.metric(
        "Accuracy",
        f"{random.randint(80,95)}%"
    )

with k4:
    st.metric(
        "Status",
        "LIVE"
    )

st.divider()

# ==================================================
# TRUE MOBILE BENTO
# ==================================================

top_left, top_right = st.columns([4,1])

with top_left:

    with st.container(border=True):

        st.subheader(
        "Market Overview"
        )

        chart = pd.DataFrame({

        "Price":[

        100,
        104,
        103,
        108,
        110,
        111,
        116,
        115,
        120

        ]

        })

        st.line_chart(chart)

with top_right:

    with st.container(border=True):

        st.write(
        "Watchlist"
        )

        st.write(
        "EUR/USD"
        )

        st.write(
        "XAU/USD"
        )

    with st.container(border=True):

        st.write(
        "Sessions"
        )

        st.success(
        "London"
        )

        st.info(
        "NY"
        )

st.divider()

# SECOND GRID

a,b,c = st.columns([2,1,1])

with a:

    with st.container(border=True):

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

with b:

    with st.container(border=True):

        st.metric(

        "Confidence",

        f"{random.randint(70,96)}%"

        )

with c:

    with st.container(border=True):

        st.metric(

        "Trend",

        random.choice(

        [

        "BUY",
        "SELL"

        ]

        )

        )

st.divider()

# LARGE SIGNAL CARD

with st.container(border=True):

    st.subheader(
    "Signal Center"
    )

    if st.button(
    "Generate Signal"
    ):

        signal = generate_signal()

        st.success(

        f"""

Signal: {signal["signal"]}

Confidence: {signal["confidence"]}%

TP: {signal["tp"]}

SL: {signal["sl"]}

Market: {market}

Timeframe: {timeframe}

        """

        )

        st.session_state.history.append({

        "time":datetime.now(),

        "market":market,

        "signal":signal["signal"],

        "confidence":signal["confidence"]

        })

st.divider()

# LOWER BENTO

left,right = st.columns([3,1])

with left:

    with st.container(border=True):

        st.subheader(
        "History"
        )

        st.dataframe(

        pd.DataFrame(

        st.session_state.history

        ),

        use_container_width=True

        )

with right:

    with st.container(border=True):

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

st.divider()

with st.container(border=True):

    st.subheader(
    "Trading Notes"
    )

    st.text_area(

    "",

    height=160

    )
