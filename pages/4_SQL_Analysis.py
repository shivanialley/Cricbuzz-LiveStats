import streamlit as st
import pandas as pd
from databases.db_connection import get_connection
import analytics.sql_queries as q

st.title("📊 SQL Analytics")

query_map = {
    "Q1 – Indian Players": q.QUERY_1,
    "Q2 – Recent Matches": q.QUERY_2,
    "Q3 – Top ODI Scorers": q.QUERY_3,
    "Q4 – Large Venues": q.QUERY_4,
    "Q5 – Team Wins": q.QUERY_5,
    "Q6 – Player Roles": q.QUERY_6,
    "Q7 – Highest Scores": q.QUERY_7,
    "Q8 – Series in 2024": q.QUERY_8,
    "Q9 – All-Rounders": q.QUERY_9,
    "Q10 – Last Matches": q.QUERY_10,
    "Q11 – Multi Format": q.QUERY_11,
    "Q12 – Home vs Away": q.QUERY_12,
    "Q13 – Partnerships": q.QUERY_13,
    "Q14 – Bowling Venues": q.QUERY_14,
    "Q15 – Close Matches": q.QUERY_15,
    "Q16 – Yearly Batting": q.QUERY_16,
    "Q17 – Toss Advantage": q.QUERY_17,
    "Q18 – Economical Bowlers": q.QUERY_18,
    "Q19 – Consistency": q.QUERY_19,
    "Q20 – Match Count": q.QUERY_20,
    "Q21 – Player Ranking": q.QUERY_21,
    "Q22 – Head to Head": q.QUERY_22,
    "Q23 – Recent Form": q.QUERY_23,
    "Q24 – Partnerships Ranking": q.QUERY_24,
    "Q25 – Time Series": q.QUERY_25,
}

selected = st.selectbox("Select Query", query_map.keys())

conn = get_connection()
df = pd.read_sql(query_map[selected], conn)

st.dataframe(df)
