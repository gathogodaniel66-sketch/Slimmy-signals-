import streamlit as st

def login():

    st.sidebar.title("User Login")

    username = st.sidebar.text_input(
        "Username"
    )

    password = st.sidebar.text_input(
        "Password",
        type="password"
    )

    if st.sidebar.button("Login"):

        st.success(
            f"Welcome {username}"
        )
