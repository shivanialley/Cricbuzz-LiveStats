import streamlit as st
import pandas as pd
import sys
import os
import time
import plotly.express as px

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import project modules
from database.db_connection import get_connection
from utils.logger import app_logger
from utils.helpers import export_to_csv, export_to_excel, export_for_powerbi

# Import tracker
import importlib.util
spec = importlib.util.spec_from_file_location("mlflow_tracking", os.path.join(project_root, "mlflow_custom", "mlflow_tracking.py"))
mlflow_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mlflow_module)
tracker = mlflow_module.tracker

st.set_page_config(page_title="Top Player Stats", page_icon="⭐", layout="wide")

st.title("⭐ Top Player Statistics")
st.markdown("Best performances across all formats")

app_logger.info("Top Player Stats page accessed")

# Create tabs for batting and bowling
tab1, tab2 = st.tabs(["🏏 Batting Statistics", "🎯 Bowling Statistics"])

# ============================================
# TAB 1: BATTING STATISTICS
# ============================================
with tab1:
    st.subheader("Top Run Scorers")
    
    # Format filter
    format_filter = st.selectbox(
        "Select Format",
        ["All Formats", "Test", "ODI", "T20I"],
        key="batting_format"
    )
    
    # Build query based on filter
    if format_filter == "All Formats":
        query = """
        SELECT 
            p.full_name AS Player,
            p.country AS Country,
            SUM(b.runs) AS Total_Runs,
            ROUND(AVG(b.runs), 2) AS Average,
            MAX(b.runs) AS Highest_Score,
            ROUND(AVG(b.strike_rate), 2) AS Strike_Rate,
            SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END) AS Centuries,
            SUM(CASE WHEN b.runs >= 50 AND b.runs < 100 THEN 1 ELSE 0 END) AS Fifties,
            COUNT(*) AS Innings
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.full_name, p.country
        ORDER BY Total_Runs DESC
        LIMIT 20
        """
    else:
        query = f"""
        SELECT 
            p.full_name AS Player,
            p.country AS Country,
            SUM(b.runs) AS Total_Runs,
            ROUND(AVG(b.runs), 2) AS Average,
            MAX(b.runs) AS Highest_Score,
            ROUND(AVG(b.strike_rate), 2) AS Strike_Rate,
            SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END) AS Centuries,
            SUM(CASE WHEN b.runs >= 50 AND b.runs < 100 THEN 1 ELSE 0 END) AS Fifties,
            COUNT(*) AS Innings
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.format = '{format_filter}'
        GROUP BY p.full_name, p.country
        ORDER BY Total_Runs DESC
        LIMIT 20
        """
    
    try:
        # Execute query and track performance
        start_time = time.time()
        conn = get_connection()
        df_batting = pd.read_sql(query, conn)
        conn.close()
        execution_time = (time.time() - start_time) * 1000
        
        # Log to MLflow
        tracker.log_query_performance(
            query_name="top_batting_stats",
            execution_time=execution_time,
            rows_returned=len(df_batting)
        )
        
        app_logger.info(f"Batting stats query executed in {execution_time:.2f}ms")
        
        # Display query performance
        st.success(f"✅ Query executed in {execution_time:.0f}ms")
        
        # Display data
        st.dataframe(
            df_batting,
            use_container_width=True,
            height=400
        )
        
        # Visualizations
        st.markdown("### 📊 Visualizations")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Bar chart - Top 10 run scorers
            fig1 = px.bar(
                df_batting.head(10),
                x='Player',
                y='Total_Runs',
                color='Country',
                title='Top 10 Run Scorers',
                labels={'Total_Runs': 'Total Runs'},
                height=400
            )
            fig1.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with viz_col2:
            # Scatter plot - Average vs Strike Rate
            fig2 = px.scatter(
                df_batting,
                x='Average',
                y='Strike_Rate',
                size='Total_Runs',
                color='Country',
                hover_data=['Player', 'Centuries', 'Fifties'],
                title='Batting Average vs Strike Rate',
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Export options
        st.markdown("### 📤 Export Options")
        export_col1, export_col2, export_col3, export_col4 = st.columns(4)
        
        with export_col1:
            if st.button("📥 Export CSV", key="batting_csv"):
                filepath = export_to_csv(df_batting, "top_batsmen")
                st.success(f"✅ Exported: `{filepath}`")
        
        with export_col2:
            if st.button("📊 Export Excel", key="batting_excel"):
                filepath = export_to_excel(df_batting, "top_batsmen")
                st.success(f"✅ Exported: `{filepath}`")
        
        with export_col3:
            if st.button("📈 Power BI Export", key="batting_pbi"):
                filepath = export_for_powerbi(df_batting, "top_batsmen")
                st.success(f"✅ Exported: `{filepath}`")
        
        with export_col4:
            csv = df_batting.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download",
                data=csv,
                file_name="top_batsmen.csv",
                mime="text/csv",
                key="batting_download"
            )
        
        # Summary statistics
        st.markdown("### 📈 Summary Statistics")
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("Players", len(df_batting))
        
        with summary_col2:
            st.metric("Total Runs", f"{df_batting['Total_Runs'].sum():,}")
        
        with summary_col3:
            st.metric("Total Centuries", int(df_batting['Centuries'].sum()))
        
        with summary_col4:
            st.metric("Avg Strike Rate", f"{df_batting['Strike_Rate'].mean():.2f}")
        
    except Exception as e:
        error_msg = f"Error fetching batting stats: {str(e)}"
        app_logger.error(error_msg)
        st.error(f"❌ {error_msg}")

# ============================================
# TAB 2: BOWLING STATISTICS
# ============================================
with tab2:
    st.subheader("Top Wicket Takers")
    
    # Format filter
    format_filter_bowl = st.selectbox(
        "Select Format",
        ["All Formats", "Test", "ODI", "T20I"],
        key="bowling_format"
    )
    
    # Build query based on filter
    if format_filter_bowl == "All Formats":
        query_bowl = """
        SELECT 
            p.full_name AS Player,
            p.country AS Country,
            SUM(w.wickets) AS Total_Wickets,
            ROUND(AVG(w.bowling_avg), 2) AS Bowling_Average,
            ROUND(AVG(w.economy), 2) AS Economy_Rate,
            SUM(w.overs) AS Total_Overs,
            COUNT(DISTINCT w.match_id) AS Matches,
            MAX(w.wickets) AS Best_Figures
        FROM bowling_stats w
        JOIN players p ON w.player_id = p.player_id
        GROUP BY p.full_name, p.country
        HAVING Total_Wickets > 0
        ORDER BY Total_Wickets DESC
        LIMIT 20
        """
    else:
        query_bowl = f"""
        SELECT 
            p.full_name AS Player,
            p.country AS Country,
            SUM(w.wickets) AS Total_Wickets,
            ROUND(AVG(w.bowling_avg), 2) AS Bowling_Average,
            ROUND(AVG(w.economy), 2) AS Economy_Rate,
            SUM(w.overs) AS Total_Overs,
            COUNT(DISTINCT w.match_id) AS Matches,
            MAX(w.wickets) AS Best_Figures
        FROM bowling_stats w
        JOIN players p ON w.player_id = p.player_id
        WHERE w.format = '{format_filter_bowl}'
        GROUP BY p.full_name, p.country
        HAVING Total_Wickets > 0
        ORDER BY Total_Wickets DESC
        LIMIT 20
        """
    
    try:
        # Execute query and track performance
        start_time = time.time()
        conn = get_connection()
        df_bowling = pd.read_sql(query_bowl, conn)
        conn.close()
        execution_time = (time.time() - start_time) * 1000
        
        # Log to MLflow
        tracker.log_query_performance(
            query_name="top_bowling_stats",
            execution_time=execution_time,
            rows_returned=len(df_bowling)
        )
        
        app_logger.info(f"Bowling stats query executed in {execution_time:.2f}ms")
        
        # Display query performance
        st.success(f"✅ Query executed in {execution_time:.0f}ms")
        
        # Display data
        st.dataframe(
            df_bowling,
            use_container_width=True,
            height=400
        )
        
        # Visualizations
        st.markdown("### 📊 Visualizations")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Bar chart - Top 10 wicket takers
            fig3 = px.bar(
                df_bowling.head(10),
                x='Player',
                y='Total_Wickets',
                color='Country',
                title='Top 10 Wicket Takers',
                labels={'Total_Wickets': 'Total Wickets'},
                height=400
            )
            fig3.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig3, use_container_width=True)
        
        with viz_col2:
            # Scatter plot - Economy vs Bowling Average
            fig4 = px.scatter(
                df_bowling,
                x='Economy_Rate',
                y='Bowling_Average',
                size='Total_Wickets',
                color='Country',
                hover_data=['Player', 'Matches', 'Best_Figures'],
                title='Economy Rate vs Bowling Average',
                height=400
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Export options
        st.markdown("### 📤 Export Options")
        export_col1, export_col2, export_col3, export_col4 = st.columns(4)
        
        with export_col1:
            if st.button("📥 Export CSV", key="bowling_csv"):
                filepath = export_to_csv(df_bowling, "top_bowlers")
                st.success(f"✅ Exported: `{filepath}`")
        
        with export_col2:
            if st.button("📊 Export Excel", key="bowling_excel"):
                filepath = export_to_excel(df_bowling, "top_bowlers")
                st.success(f"✅ Exported: `{filepath}`")
        
        with export_col3:
            if st.button("📈 Power BI Export", key="bowling_pbi"):
                filepath = export_for_powerbi(df_bowling, "top_bowlers")
                st.success(f"✅ Exported: `{filepath}`")
        
        with export_col4:
            csv = df_bowling.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download",
                data=csv,
                file_name="top_bowlers.csv",
                mime="text/csv",
                key="bowling_download"
            )
        
        # Summary statistics
        st.markdown("### 📈 Summary Statistics")
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("Bowlers", len(df_bowling))
        
        with summary_col2:
            st.metric("Total Wickets", int(df_bowling['Total_Wickets'].sum()))
        
        with summary_col3:
            st.metric("Avg Economy", f"{df_bowling['Economy_Rate'].mean():.2f}")
        
        with summary_col4:
            st.metric("Total Matches", int(df_bowling['Matches'].sum()))
        
    except Exception as e:
        error_msg = f"Error fetching bowling stats: {str(e)}"
        app_logger.error(error_msg)
        st.error(f"❌ {error_msg}")

# Sidebar info
with st.sidebar:
    st.markdown("### ⭐ Player Stats Info")
    st.info("""
    View top performing players in batting and bowling categories.
    
    **Batting Metrics:**
    - Total Runs
    - Average
    - Strike Rate
    - Centuries & Fifties
    
    **Bowling Metrics:**
    - Total Wickets
    - Bowling Average
    - Economy Rate
    - Best Figures
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Filters Available")
    st.success("""
    - Filter by Format
    - Top 20 players
    - Visual charts
    - Export options
    """)