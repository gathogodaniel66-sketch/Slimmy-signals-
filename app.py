import streamlit as st
import pandas as pd
import requests
import time
import numpy as np
from datetime import datetime
from auth import login
from config import APP_NAME, MARKETS

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📈",
    layout="wide"
)

login()

TWELVEDATA_API_KEY = "97e8ab17948f4772a17cb7dd4f8a6471"

if "history" not in st.session_state:
    st.session_state.history = []

if "bot_running" not in st.session_state:
    st.session_state.bot_running = True

if "price_history" not in st.session_state:
    st.session_state.price_history = {
        market: [100.0] for market in MARKETS
    }

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📊 SLIMMY SIGNALS")

selected_market = st.sidebar.selectbox(
    "Market",
    MARKETS
)

timeframe = st.sidebar.selectbox(
    "Signal Timeframe",
    [
        "1min",
        "5min",
        "10min",
        "30min",
        "1h"
    ]
)

refresh_rate = st.sidebar.slider(
    "Refresh Seconds",
    10,
    60,
    30
)

colA, colB = st.sidebar.columns(2)

with colA:
    if st.button("▶ Start"):
        st.session_state.bot_running = True

with colB:
    if st.button("⏹ Stop"):
        st.session_state.bot_running = False

# ---------------- DATA ---------------- #

@st.cache_data(ttl=20)
def fetch_market_data(symbol, tf):

    base = "https://api.twelvedata.com"

    try:

        price = requests.get(
            f"{base}/price?symbol={symbol}&apikey={TWELVEDATA_API_KEY}",
            timeout=10
        ).json()

        current_price = float(
            price.get(
                "price",
                st.session_state.price_history[symbol][-1]
            )
        )

        rsi = requests.get(
            f"{base}/rsi?symbol={symbol}&interval={tf}&time_period=14&apikey={TWELVEDATA_API_KEY}",
            timeout=10
        ).json()

        rsi_val = float(
            rsi["values"][0]["rsi"]
        ) if "values" in rsi else 50

        macd = requests.get(
            f"{base}/macd?symbol={symbol}&interval={tf}&apikey={TWELVEDATA_API_KEY}",
            timeout=10
        ).json()

        macd_state = "NEUTRAL"

        if "values" in macd:

            m = float(
                macd["values"][0]["macd"]
            )

            s = float(
                macd["values"][0]["macd_signal"]
            )

            macd_state = (
                "BULLISH"
                if m > s
                else "BEARISH"
            )

        adx = requests.get(
            f"{base}/adx?symbol={symbol}&interval={tf}&apikey={TWELVEDATA_API_KEY}",
            timeout=10
        ).json()

        adx_val = float(
            adx["values"][0]["adx"]
        ) if "values" in adx else 20

        atr = requests.get(
            f"{base}/atr?symbol={symbol}&interval={tf}&apikey={TWELVEDATA_API_KEY}",
            timeout=10
        ).json()

        atr_val = float(
            atr["values"][0]["atr"]
        ) if "values" in atr else 0

        ts = requests.get(
            f"{base}/time_series?symbol={symbol}&interval={tf}&outputsize=20&apikey={TWELVEDATA_API_KEY}",
            timeout=10
        ).json()

        volume_ok = True

        if "values" in ts:

            vols = [
                float(v.get("volume",0))
                for v in ts["values"]
                if "volume" in v
            ]

            if len(vols) > 5:

                volume_ok = (
                    vols[0] >= np.mean(vols)
                )

        return (
            current_price,
            rsi_val,
            macd_state,
            adx_val,
            atr_val,
            volume_ok
        )

    except Exception as e:

        st.warning(
            f"API Error: {e}"
        )

        return (
            st.session_state.price_history[symbol][-1],
            50,
            "NEUTRAL",
            20,
            0,
            True
        )

# ---------------- STRATEGY ---------------- #

def evaluate_strategy(
    prices,
    rsi,
    macd,
    adx,
    atr,
    volume_ok
):

    if len(prices) < 20:

        return "HOLD",50,55

    fast = np.mean(
        prices[-5:]
    )

    slow = np.mean(
        prices[-20:]
    )

    score = 0

    if fast > slow:
        score += 25
    else:
        score -= 25

    if macd == "BULLISH":
        score += 20

    if macd == "BEARISH":
        score -= 20

    if 35 < rsi < 65:
        score += 15

    if adx > 25:
        score += 20

    if atr > 0:
        score += 10

    if volume_ok:
        score += 10

    if adx < 20:
        return "HOLD",45,55

    confidence = min(
        abs(score),
        95
    )

    accuracy = min(
        55 + int(confidence/2),
        75
    )

    if score >= 60:
        return "BUY",confidence,accuracy

    elif score <= -40:
        return "SELL",confidence,accuracy

    return "HOLD",confidence,accuracy

# ---------------- EXECUTION ---------------- #

(
price,
rsi,
macd,
adx,
atr,
volume_ok
) = fetch_market_data(
    selected_market,
    timeframe
)

if st.session_state.bot_running:

    st.session_state.price_history[
        selected_market
    ].append(price)

    if len(
        st.session_state.price_history[
            selected_market
        ]
    ) > 200:

        st.session_state.price_history[
            selected_market
        ].pop(0)

signal, confidence, accuracy = evaluate_strategy(
    st.session_state.price_history[
        selected_market
    ],
    rsi,
    macd,
    adx,
    atr,
    volume_ok
)

# ---------------- TP SL ---------------- #

risk = 1.5

if signal == "BUY":

    sl = round(
        price - atr,
        2
    )

    tp = round(
        price + atr*risk,
        2
    )

elif signal == "SELL":

    sl = round(
        price + atr,
        2
    )

    tp = round(
        price - atr*risk,
        2
    )

else:

    sl = "-"
    tp = "-"

# ---------------- UI ---------------- #

st.title(APP_NAME)

c1,c2,c3 = st.columns(3)

with c1:
    st.metric(
        "Price",
        round(price,2)
    )

with c2:
    st.metric(
        "Signal",
        signal
    )

with c3:
    st.metric(
        "Confidence",
        f"{confidence}%"
    )

d1,d2,d3 = st.columns(3)

with d1:
    st.metric(
        "RSI",
        round(rsi,2)
    )

with d2:
    st.metric(
        "ADX",
        round(adx,2)
    )

with d3:
    st.metric(
        "ATR",
        round(atr,2)
    )

st.success(f"""

Signal: {signal}

Entry: {price}

Take Profit: {tp}

Stop Loss: {sl}

Timeframe: {timeframe}

Estimated Accuracy: {accuracy}%

""")

st.caption(
    f"Updated {datetime.now().strftime('%H:%M:%S')}"
)

chart = pd.DataFrame({
    "Price":
    st.session_state.price_history[
        selected_market
    ]
})

st.line_chart(
    chart,
    use_container_width=True
)

if st.button(
    "Save Signal"
):

    st.session_state.history.append({

        "time":
        datetime.now(),

        "market":
        selected_market,

        "signal":
        signal,

        "tp":
        tp,

        "sl":
        sl,

        "confidence":
        confidence
    })

if st.session_state.history:

    st.dataframe(
        pd.DataFrame(
            st.session_state.history
        )
    )

if st.session_state.bot_running:

    time.sleep(
        refresh_rate
    )

    st.rerun()
