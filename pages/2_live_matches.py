import streamlit as st
from api.cricbuzz_api import get_live_matches

st.title("🔴 Live Matches")

try:
    data = get_live_matches()
    st.json(data)
except Exception as e:
    st.error(str(e))
