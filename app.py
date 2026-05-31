import streamlit as st
import pandas as pd
import random
from scanner import generate_signal
from auth import login
from config import APP_NAME, MARKETS

st.set_page_config(
    layout="wide",
    page_title=APP_NAME
)

login()

st.markdown("""

<style>

.stApp{
background:linear-gradient(
180deg,
#07101D,
#081A32
);
color:white;
}

.card{

background:rgba(18,26,45,0.9);

border:1px solid rgba(
255,255,255,0.08
);

border-radius:28px;

padding:25px;

box-shadow:
0 0 30px rgba(
0,120,255,.08
);

margin-bottom:18px;

}

.big-text{

font-size:60px;
font-weight:bold;

}

.small{

opacity:.7;

font-size:14px;

}

</style>

""",unsafe_allow_html=True)

st.caption(
"Professional Multi Market Dashboard"
)

# HERO GRID

left,right = st.columns([2,1])

with left:

    st.markdown("""

<div class="card">

STATUS & PRICE

<br><br>

<div class="small">
STATUS:
</div>

<div class="big-text">

LIVE

</div>

</div>

""",unsafe_allow_html=True)

with right:

    st.markdown(f"""

<div class="card">

ACCURACY

<br><br>

<div class="big-text">

{random.randint(80,95)}%

</div>

</div>

""",unsafe_allow_html=True)

# SECOND ROW

a,b,c = st.columns(3)

with a:

    st.markdown(f"""

<div class="card">

MARKETS

<div class="big-text">

{len(MARKETS)}

</div>

</div>

""",unsafe_allow_html=True)

with b:

    st.markdown("""

<div class="card">

SIGNALS

<div class="big-text">

0

</div>

</div>

""",unsafe_allow_html=True)

with c:

    st.markdown("""

<div class="card">

SUBSCRIPTION PLAN

<br>

PROFESSIONAL

</div>

""",unsafe_allow_html=True)

# LARGE PANEL

st.markdown("""

<div class="card">

<h1>

Market Overview

</h1>

</div>

""",unsafe_allow_html=True)

chart = pd.DataFrame({

"Price":[

100,
102,
105,
107,
109,
112,
115,
114,
118

]

})

st.line_chart(
chart,
height=400
)

st.divider()

market = st.selectbox(

"Market",

MARKETS

)

if st.button(
"Generate Signal"
):

    signal = generate_signal()

    st.success(

    f"""

Signal:

{signal["signal"]}

Confidence:

{signal["confidence"]}%

    """

    )
