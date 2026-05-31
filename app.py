import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# =====================================================
# API KEY
# =====================================================

API_KEY = "97e8ab17948f4772a17cb7dd4f8a6471"

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI MAJIQ CLOUD PRO",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#020617,#07111f,#020617);
    color:white;
}

.title{
    font-size:55px;
    font-weight:bold;
    color:#72ffb6;
}

.card{
    background:rgba(255,255,255,0.05);
    border-radius:20px;
    padding:20px;
    margin-bottom:20px;
    border:1px solid rgba(255,255,255,0.08);
}

.buy{
    color:#00ff99;
    font-size:28px;
    font-weight:bold;
}

.sell{
    color:#ff4d4d;
    font-size:28px;
    font-weight:bold;
}

.neutral{
    color:orange;
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOGIN
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():

    st.markdown(
        '<p class="title">AI MAJIQ CLOUD PRO</p>',
        unsafe_allow_html=True
    )

    st.subheader("Professional AI Trading Scanner")

    user = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("LOGIN"):

        if user and password:

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error("Enter username and password")

# =====================================================
# MARKETS
# =====================================================

markets = {

    "EUR/USD": "EUR/USD",
    "GBP/USD": "GBP/USD",
    "USD/JPY": "USD/JPY",
    "AUD/USD": "AUD/USD",
    "XAU/USD": "XAU/USD",
    "BTC/USD": "BTC/USD",
    "ETH/USD": "ETH/USD"
}

# =====================================================
# RSI
# =====================================================

def calculate_rsi(close, period=14):

    delta = close.diff()

    gain = delta.clip(lower=0)

    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# =====================================================
# MACD
# =====================================================

def calculate_macd(close):

    ema12 = close.ewm(span=12).mean()

    ema26 = close.ewm(span=26).mean()

    macd = ema12 - ema26

    signal = macd.ewm(span=9).mean()

    return macd, signal

# =====================================================
# FETCH DATA
# =====================================================

def get_market_data(symbol, interval):

    try:

        url = (
            f"https://api.twelvedata.com/time_series?"
            f"symbol={symbol}"
            f"&interval={interval}"
            f"&outputsize=100"
            f"&apikey={API_KEY}"
        )

        response = requests.get(url)

        data = response.json()

        if "values" not in data:
            return None

        df = pd.DataFrame(data["values"])

        df = df.iloc[::-1]

        df["close"] = df["close"].astype(float)

        return df

    except:
        return None

# =====================================================
# SIGNAL ENGINE
# =====================================================

def scan_market(symbol, interval):

    df = get_market_data(symbol, interval)

    if df is None:
        return None

    close = df["close"]

    current_price = close.iloc[-1]

    # EMA

    ema20 = close.ewm(span=20).mean().iloc[-1]

    ema50 = close.ewm(span=50).mean().iloc[-1]

    # RSI

    rsi = calculate_rsi(close).iloc[-1]

    # MACD

    macd, macd_signal = calculate_macd(close)

    macd_value = macd.iloc[-1]

    macd_signal_value = macd_signal.iloc[-1]

    # SCORE

    score = 0

    if ema20 > ema50:
        score += 1
    else:
        score -= 1

    if rsi > 55:
        score += 1

    elif rsi < 45:
        score -= 1

    if macd_value > macd_signal_value:
        score += 1
    else:
        score -= 1

    # SIGNAL

    if score >= 2:
        signal = "BUY"

    elif score <= -2:
        signal = "SELL"

    else:
        signal = "NEUTRAL"

    confidence = abs(score) * 33

    # TP / SL

    if signal == "BUY":

        tp = round(current_price * 1.01, 4)

        sl = round(current_price * 0.995, 4)

    elif signal == "SELL":

        tp = round(current_price * 0.99, 4)

        sl = round(current_price * 1.005, 4)

    else:

        tp = current_price
        sl = current_price

    return {

        "price": round(current_price, 4),
        "signal": signal,
        "confidence": confidence,
        "ema20": round(ema20, 4),
        "ema50": round(ema50, 4),
        "rsi": round(rsi, 2),
        "macd": round(macd_value, 4),
        "tp": tp,
        "sl": sl
    }

# =====================================================
# DASHBOARD
# =====================================================

def dashboard():

    st.markdown(
        '<p class="title">LIVE AI SIGNAL SCANNER</p>',
        unsafe_allow_html=True
    )

    st.success("20+ UPGRADES ACTIVE")

    timeframe = st.selectbox(
        "Select Timeframe",
        ["5min", "15min", "30min", "1h", "4h", "1day"]
    )

    auto_refresh = st.checkbox("Auto Refresh")

    if auto_refresh:

        time.sleep(30)

        st.rerun()

    if st.button("SCAN LIVE MARKET"):

        total = 0

        for pair, symbol in markets.items():

            result = scan_market(
                symbol,
                timeframe
            )

            if result:

                total += 1

                if result["signal"] == "BUY":
                    cls = "buy"

                elif result["signal"] == "SELL":
                    cls = "sell"

                else:
                    cls = "neutral"

                st.markdown(f"""

                <div class="card">

                <h2>{pair}</h2>

                <p class="{cls}">
                {result["signal"]}
                </p>

                <b>Live Entry:</b>
                {result["price"]}<br><br>

                <b>RSI:</b>
                {result["rsi"]}<br>

                <b>EMA20:</b>
                {result["ema20"]}<br>

                <b>EMA50:</b>
                {result["ema50"]}<br>

                <b>MACD:</b>
                {result["macd"]}<br>

                <b>Confidence:</b>
                {result["confidence"]}%<br>

                <b>Take Profit:</b>
                {result["tp"]}<br>

                <b>Stop Loss:</b>
                {result["sl"]}<br>

                <b>Updated:</b>
                {datetime.now().strftime("%H:%M:%S")}

                </div>

                """, unsafe_allow_html=True)

        st.success(f"{total} LIVE SIGNALS GENERATED")

# =====================================================
# ROUTER
# =====================================================

if st.session_state.logged_in:
    dashboard()
else:
    login_page()
