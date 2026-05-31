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
.stApp {
    background: #08111F;
    color: white;
}

section[data-testid="stSidebar"] {
    background: #111827;
}

/* Customizing Streamlit's default metric tiles for a sleek dark Bento look */
[data-testid="stMetric"] {
    background: #131E30;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #24324A;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Custom container classes for varied Bento block sizes */
.bento-block {
    background: #131E30;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #24324A;
    margin-bottom: 16px;
}

.bento-status-live {
    color: #4ADE80;
    font-weight: bold;
    font-size: 1.2rem;
}

.micro-text {
    font-size: 0.8rem;
    color: #9CA3AF;
}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("📊 SLIMMY SIGNALS")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "History", "Analytics"]
)

# ---------------- HEADER ---------------- #
st.title(APP_NAME)
st.caption("Professional Multi Market Dashboard")

# ---------------- KPI BENTO GRID (ROW 1) ---------------- #
# We arrange this into a 3-column layout where the 'Status' block spans slightly wider to host extra micro-data
k_col1, k_col2, k_col3 = st.columns([2, 1, 1])

with k_col1:
    # Combining Status & Price indicators into a larger Bento tile as seen in watermarked_img_873913139780230313.png
    with st.container(border=True):
        st.markdown("<p class='micro-text'>STATUS & PRICE</p>", unsafe_allow_html=True)
        
        # Internal columns inside the card block
        status_left, status_right = st.columns([1, 1])
        with status_left:
            st.markdown("### STATUS:<br><span class='bento-status-live'>● LIVE</span>", unsafe_allow_html=True)
        with status_right:
            st.markdown(
                """
                <div style="background: #0B1320; padding: 10px; border-radius: 8px; border: 1px solid #1E293B;">
                    <p class='micro-text' style='margin:0;'>index: <b>5</b></p>
                    <p class='micro-text' style='margin:0;'>Price: <b>111</b></p>
                </div>
                """, 
                unsafe_allow_html=True
            )

with k_col2:
    st.metric(
        label="Accuracy 📈",
        value=f"{random.randint(80,95)}%",
        delta="↑ High"
    )

with k_col3:
    # We can place another subscription or tier metric next to it to complete the balanced grid row
    with st.container(border=True):
        st.markdown("<p class='micro-text'>SUBSCRIPTION PLAN</p>", unsafe_allow_html=True)
        st.markdown("### PROFESSIONAL")
        st.markdown("<span class='bento-status-live'>● Active</span>", unsafe_allow_html=True)


# ---------------- KPI BENTO GRID (ROW 2) ---------------- #
# Sub-metrics aligned tightly underneath the main data status blocks
k_sub1, k_sub2, k_sub3 = st.columns([1, 1, 2])

with k_sub1:
    st.metric(
        label="Markets 🎛️",
        value=len(MARKETS)
    )

with k_sub2:
    st.metric(
        label="Signals 📡",
        value=len(st.session_state.history)
    )

with k_sub3:
    with st.container(border=True):
        st.markdown("<p class='micro-text'>SESSION FOCUS</p>", unsafe_allow_html=True)
        sess_1, sess_2 = st.columns(2)
        sess_1.success("London Open")
        sess_2.info("NY Session")


st.divider()

# ---------------- MARKET OVERVIEW BENTO (ROW 3) ---------------- #
top_left, top_right = st.columns([3, 1])

with top_left:
    with st.container(border=True):
        st.subheader("Market Overview")
        chart = pd.DataFrame({
            "Price": [100, 104, 103, 108, 110, 111, 116, 115, 120]
        })
        st.line_chart(chart, use_container_width=True)

with top_right:
    with st.container(border=True):
        st.markdown("**Watchlist**")
        st.caption("⚡ Top Assets")
        st.write("🔹 EUR/USD")
        st.write("🔹 GBP/USD")
        st.write("🔹 USD/JPY")

st.divider()

# ---------------- SIGNAL GENERATOR GRID ---------------- #
a, b, c = st.columns([2, 1, 1])

with a:
    with st.container(border=True):
        market = st.selectbox("Market", MARKETS)
        timeframe = st.selectbox("Timeframe", ["M5", "M15", "H1", "H4"])

with b:
    with st.container(border=True):
        st.metric("Confidence", f"{random.randint(70,96)}%")

with c:
    with st.container(border=True):
        st.metric("Trend", random.choice(["BUY", "SELL"]))

st.divider()

# LARGE SIGNAL CARD
with st.container(border=True):
    st.subheader("Signal Center")
    if st.button("Generate Signal", use_container_width=True):
        signal = generate_signal()
        st.success(
            f"""
            **Signal:** {signal["signal"]}  
            **Confidence:** {signal["confidence"]}%  
            **TP:** {signal["tp"]} | **SL:** {signal["sl"]}  
            **Market:** {market} | **Timeframe:** {timeframe}
            """
        )
        st.session_state.history.append({
            "time": datetime.now(),
            "market": market,
            "signal": signal["signal"],
            "confidence": signal["confidence"]
        })

st.divider()

# LOWER BENTO (HISTORY & ANALYTICS)
left, right = st.columns([2, 1])

with left:
    with st.container(border=True):
        st.subheader("History")
        st.dataframe(
            pd.DataFrame(st.session_state.history),
            use_container_width=True
        )

with right:
    with st.container(border=True):
        st.subheader("Analytics")
        if len(st.session_state.history) > 0:
            df = pd.DataFrame(st.session_state.history)
            st.bar_chart(df["confidence"])
        else:
            st.info("No signal data available yet.")

st.divider()

with st.container(border=True):
    st.subheader("Trading Notes")
    st.text_area("", height=120, placeholder="Write down structural key zones or thoughts...")
