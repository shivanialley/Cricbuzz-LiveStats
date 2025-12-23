import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    layout="wide"
)

st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")

st.write("""
Navigate using the sidebar to:
- View live matches
- Explore player statistics
- Run SQL analytics
- Perform CRUD operations
""")
