import streamlit as st
from database.crud import add_player, get_players, delete_player

st.title("🛠 CRUD Operations")

with st.form("add_player"):
    pid = st.number_input("Player ID", step=1)
    name = st.text_input("Name")
    country = st.text_input("Country")
    role = st.text_input("Role")
    bat = st.text_input("Batting Style")
    bowl = st.text_input("Bowling Style")

    submitted = st.form_submit_button("Add Player")

    if submitted:
        add_player((pid, name, country, role, bat, bowl))
        st.success("Player added!")

st.subheader("All Players")
players = get_players()
st.table(players)
