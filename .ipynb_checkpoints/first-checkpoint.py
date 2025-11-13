import streamlit as st

st.set_page_config(
    page_title="BFH",
    page_icon="🍱",
)

st.title("Welcome to Better Food Habits!👋")
st.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.success("Select a recommendation app.")

st.markdown(
"""
Welcome to Better Food Habits! Your personalized nutrition assistant for healthier living. Get tailored meal recommendations, expert insights, and intuitive tracking features to support your wellness goals. Join us today and start your journey towards a healthier you.
"""
)