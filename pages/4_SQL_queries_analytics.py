import streamlit as st
import pandas as pd
import sys
import os
import time

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import project modules
from database.db_connection import get_connection
from analytics.sql_queries import *
from utils.logger import app_logger
from utils.helpers import export_to_csv, export_for_powerbi, generate_report

# Import tracker
import importlib.util
spec = importlib.util.spec_from_file_location("mlflow_tracking", os.path.join(project_root, "mlflow_custom", "mlflow_tracking.py"))
mlflow_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mlflow_module)
tracker = mlflow_module.tracker

st.set_page_config(page_title="SQL Analytics", page_icon="📊", layout="wide")

st.title("📊 SQL Analytics Dashboard")
st.markdown("Execute 25+ analytical queries on cricket database")

app_logger.info("SQL Analytics page accessed")

# Query dictionary organized by difficulty
query_dict = {
    "Beginner (1-8)": {
        "Q1: Indian Players": QUERY_1,
        "Q2: Recent Matches (Last 7 Days)": QUERY_2,
        "Q3: Top 10 ODI Run Scorers": QUERY_3,
        "Q4: Large Venues (>25K Capacity)": QUERY_4,
        "Q5: Team Win Counts": QUERY_5,
        "Q6: Players by Role": QUERY_6,
        "Q7: Highest Score by Format": QUERY_7,
        "Q8: 2024 Series": QUERY_8,
    },
    "Intermediate (9-16)": {
        "Q9: All-rounder Performance (1000+ runs, 50+ wickets)": QUERY_9,
        "Q10: Last 20 Completed Matches": QUERY_10,
        "Q11: Multi-Format Players Performance": QUERY_11,
        "Q12: Home vs Away Win Analysis": QUERY_12,
        "Q13: Partnerships (100+ runs)": QUERY_13,
        "Q14: Venue-Specific Bowling Performance": QUERY_14,
        "Q15: Close Match Performers": QUERY_15,
        "Q16: Yearly Performance Trends (Since 2020)": QUERY_16,
    },
    "Advanced (17-25)": {
        "Q17: Toss Decision Impact on Wins": QUERY_17,
        "Q18: Most Economical Bowlers (10+ matches)": QUERY_18,
        "Q19: Batting Consistency Analysis": QUERY_19,
        "Q20: Format-wise Match Participation (20+ matches)": QUERY_20,
        "Q21: Comprehensive Player Ranking System": QUERY_21,
        "Q22: Head-to-Head Team Records (3 years)": QUERY_22,
        "Q23: Recent Form Analysis (6 months)": QUERY_23,
        "Q24: Best Batting Partnerships (5+ partnerships)": QUERY_24,
        "Q25: Quarterly Performance Trends": QUERY_25,
    }
}

# Query descriptions
query_descriptions = {
    "Q1: Indian Players": "List all players representing India with their playing roles and styles.",
    "Q2: Recent Matches (Last 7 Days)": "Show matches played in the last 7 days with venue details.",
    "Q3: Top 10 ODI Run Scorers": "Top 10 batsmen in ODI format by total runs with centuries count.",
    "Q4: Large Venues (>25K Capacity)": "Cricket venues with seating capacity over 25,000.",
    "Q5: Team Win Counts": "Total wins for each team across all matches.",
    "Q6: Players by Role": "Distribution of players by their playing roles.",
    "Q7: Highest Score by Format": "Highest individual score in each cricket format.",
    "Q8: 2024 Series": "All cricket series that started in 2024.",
    "Q9: All-rounder Performance (1000+ runs, 50+ wickets)": "All-rounders with significant contributions in both batting and bowling.",
    "Q10: Last 20 Completed Matches": "Most recent 20 matches with results and venue information.",
    "Q11: Multi-Format Players Performance": "Players who performed in 2+ formats with format-wise runs.",
    "Q12: Home vs Away Win Analysis": "Team performance when playing at home vs away venues.",
    "Q13: Partnerships (100+ runs)": "Batting partnerships where consecutive batsmen scored 100+ combined runs.",
    "Q14: Venue-Specific Bowling Performance": "Bowlers' statistics at specific venues (minimum 3 matches).",
    "Q15: Close Match Performers": "Player performance in close matches (decided by <50 runs or <5 wickets).",
    "Q16: Yearly Performance Trends (Since 2020)": "Player performance evolution year by year since 2020.",
    "Q17: Toss Decision Impact on Wins": "Win percentage analysis based on toss decision (bat/bowl first).",
    "Q18: Most Economical Bowlers (10+ matches)": "Bowlers with best economy rates in limited-overs cricket.",
    "Q19: Batting Consistency Analysis": "Measure batting consistency using standard deviation.",
    "Q20: Format-wise Match Participation (20+ matches)": "Players who played 20+ matches across formats.",
    "Q21: Comprehensive Player Ranking System": "Weighted scoring system combining batting, bowling, and fielding.",
    "Q22: Head-to-Head Team Records (3 years)": "Team vs team records from last 3 years (minimum 5 matches).",
    "Q23: Recent Form Analysis (6 months)": "Player form in last 6 months (minimum 5 matches).",
    "Q24: Best Batting Partnerships (5+ partnerships)": "Most successful batting pairs based on average partnership runs.",
    "Q25: Quarterly Performance Trends": "Player performance analyzed by quarters with minimum 3 matches.",
}

# Sidebar - Query Selection
st.sidebar.header("🔍 Query Selection")
category = st.sidebar.selectbox(
    "Select Difficulty Level",
    list(query_dict.keys())
)

query_name = st.sidebar.selectbox(
    "Select Query",
    list(query_dict[category].keys())
)

selected_query = query_dict[category][query_name]

# Display query description
st.info(f"**Query Description:** {query_descriptions.get(query_name, 'N/A')}")

# Display SQL Query
with st.expander("📝 View SQL Query", expanded=False):
    st.code(selected_query, language="sql")
    
    # Copy to clipboard button
    if st.button("📋 Copy Query"):
        st.code(selected_query, language="sql")
        st.success("✅ Query displayed above - copy manually")

st.markdown("---")

# Execute Query Button
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    execute_button = st.button("▶️ Execute Query", type="primary", use_container_width=True)

with col2:
    limit_results = st.checkbox("Limit to 100 rows", value=False)

with col3:
    show_stats = st.checkbox("Show Statistics", value=True)

# Execute query when button is clicked
if execute_button:
    try:
        with st.spinner("⏳ Executing query..."):
            # Track execution time
            start_time = time.time()
            
            # Connect and execute
            conn = get_connection()
            df = pd.read_sql(selected_query, conn)
            conn.close()
            
            execution_time = (time.time() - start_time) * 1000
            
            # Apply limit if checkbox is checked
            if limit_results and len(df) > 100:
                df_display = df.head(100)
                limited = True
            else:
                df_display = df
                limited = False
            
            # Log to MLflow
            tracker.log_query_performance(
                query_name=query_name,
                execution_time=execution_time,
                rows_returned=len(df)
            )
            
            app_logger.info(f"Query '{query_name}' executed in {execution_time:.2f}ms, returned {len(df)} rows")
        
        # Display success message
        st.success(f"✅ Query executed successfully in {execution_time:.0f}ms")
        
        # Display row info
        if limited:
            st.warning(f"⚠️ Showing first 100 rows out of {len(df)} total rows")
        else:
            st.info(f"📊 Query returned {len(df)} rows")
        
        # Display results
        st.subheader("📋 Query Results")
        st.dataframe(
            df_display,
            use_container_width=True,
            height=400
        )
        
        # Statistics section
        if show_stats and len(df) > 0:
            st.markdown("---")
            st.subheader("📈 Result Statistics")
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("Total Rows", len(df))
            
            with stat_col2:
                st.metric("Total Columns", len(df.columns))
            
            with stat_col3:
                st.metric("Execution Time", f"{execution_time:.0f}ms")
            
            with stat_col4:
                memory_usage = df.memory_usage(deep=True).sum() / 1024  # KB
                st.metric("Memory Usage", f"{memory_usage:.1f} KB")
            
            # Column information
            with st.expander("📊 Column Information"):
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.values,
                    'Non-Null Count': df.count().values,
                    'Null Count': df.isnull().sum().values
                })
                st.dataframe(col_info, use_container_width=True)
            
            # Numeric columns summary
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                with st.expander("🔢 Numeric Columns Summary"):
                    st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        
        # Export Options
        st.markdown("---")
        st.subheader("📤 Export Options")
        
        export_col1, export_col2, export_col3, export_col4 = st.columns(4)
        
        with export_col1:
            if st.button("📥 Export to CSV"):
                filepath = export_to_csv(df, query_name.replace(" ", "_").replace(":", ""))
                st.success(f"✅ Saved to: `{filepath}`")
                app_logger.info(f"Query results exported to CSV: {filepath}")
        
        with export_col2:
            if st.button("📊 Export for Power BI"):
                filepath = export_for_powerbi(df, query_name.replace(" ", "_").replace(":", ""))
                st.success(f"✅ Saved to: `{filepath}`")
                st.info("💡 Import this file in Power BI Desktop")
                app_logger.info(f"Query results exported for Power BI: {filepath}")
        
        with export_col3:
            if st.button("📄 Generate Report"):
                report_content = f"""
Query: {query_name}
Category: {category}
Execution Time: {execution_time:.2f}ms
Rows Returned: {len(df)}
Columns: {len(df.columns)}

Results:
{df.to_string()}
"""
                filepath = generate_report(report_content, query_name.replace(" ", "_").replace(":", ""))
                st.success(f"✅ Report saved to: `{filepath}`")
                app_logger.info(f"Report generated: {filepath}")
        
        with export_col4:
            # Direct download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"{query_name.replace(' ', '_')}.csv",
                mime="text/csv"
            )
        
    except Exception as e:
        error_msg = f"Query execution failed: {str(e)}"
        app_logger.error(f"{error_msg} | Query: {query_name}")
        st.error(f"❌ {error_msg}")
        
        # Show error details
        with st.expander("🔧 Error Details"):
            st.code(str(e))
            st.markdown("""
            **Common Issues:**
            - **Syntax Error**: Check SQL syntax in query
            - **Column Not Found**: Table structure might have changed
            - **Connection Error**: Database might be down
            - **Permission Error**: Check database user permissions
            
            **Solutions:**
            - Verify database is initialized: `python init_db.py`
            - Check MySQL is running: `sudo systemctl status mysql`
            - Review error message above for specific issue
            """)

else:
    # Show placeholder when no query executed
    st.info("👆 Click '▶️ Execute Query' button to run the selected SQL query")
    
    # Show query stats from MLflow if available
    st.markdown("---")
    st.subheader("📊 Query Performance History")
    st.markdown("""
    View detailed query performance metrics in [MLflow Dashboard](http://localhost:5000)
    
    **Metrics Tracked:**
    - Execution time for each query
    - Number of rows returned
    - Query execution frequency
    - Performance trends over time
    """)

# Sidebar additional info
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📚 Query Categories")
    
    st.markdown("""
    **Beginner (1-8)**
    - Basic SELECT, WHERE
    - Simple aggregations
    - ORDER BY, LIMIT
    
    **Intermediate (9-16)**
    - JOINs (2-3 tables)
    - Subqueries
    - GROUP BY with HAVING
    - CASE statements
    
    **Advanced (17-25)**
    - Window functions
    - CTEs (Common Table Expressions)
    - Statistical functions
    - Complex aggregations
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.success("""
    - Review query before executing
    - Use limit for large results
    - Export data for analysis
    - Check MLflow for performance
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Resources")
    st.markdown("- [SQL Tutorial](https://www.w3schools.com/sql/)")
    st.markdown("- [MySQL Docs](https://dev.mysql.com/doc/)")
    st.markdown("- [MLflow Dashboard](http://localhost:5000)")