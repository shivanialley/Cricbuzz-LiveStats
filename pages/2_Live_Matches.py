import streamlit as st
import pandas as pd
import sys
import os
import time

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import project modules
from api.cricbuzz_api import get_live_matches
from utils.logger import api_logger
from utils.helpers import export_to_csv, export_for_powerbi

# Import tracker using exec to avoid module conflicts
import importlib.util
spec = importlib.util.spec_from_file_location("mlflow_tracking", os.path.join(project_root, "mlflow_custom", "mlflow_tracking.py"))
mlflow_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mlflow_module)
tracker = mlflow_module.tracker

st.set_page_config(page_title="Live Matches", page_icon="🏏", layout="wide")

st.title("🏏 Live Cricket Matches")
st.markdown("Real-time match updates from Cricbuzz API")

api_logger.info("Live Matches page accessed")

# Add refresh button
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh Matches"):
        st.rerun()

st.markdown("---")

try:
    # Show loading spinner
    with st.spinner("⏳ Fetching live matches..."):
        # Track API call time
        start_time = time.time()
        matches_data = get_live_matches()
        response_time = (time.time() - start_time) * 1000
        
        # Log to MLflow
        tracker.log_api_call(
            endpoint="/matches/v1/live",
            response_time=response_time,
            status_code=200,
            data_size=len(str(matches_data))
        )
        
        api_logger.info(f"Live matches fetched successfully in {response_time:.2f}ms")
    
    # Display API performance
    st.success(f"✅ Data fetched in {response_time:.0f}ms")
    
    # Parse match data
    if 'typeMatches' in matches_data:
        all_matches = []
        
        for match_type in matches_data['typeMatches']:
            series_list = match_type.get('seriesMatches', [])
            
            for series in series_list:
                if 'seriesAdWrapper' in series:
                    series_info = series['seriesAdWrapper']
                    series_name = series_info.get('seriesName', 'Unknown Series')
                    
                    matches = series_info.get('matches', [])
                    
                    for match in matches:
                        if 'matchInfo' in match:
                            match_info = match['matchInfo']
                            
                            # Extract match details
                            match_dict = {
                                'Series': series_name,
                                'Match': match_info.get('matchDesc', 'N/A'),
                                'Team 1': match_info.get('team1', {}).get('teamName', 'TBA'),
                                'Team 2': match_info.get('team2', {}).get('teamName', 'TBA'),
                                'Venue': match_info.get('venueInfo', {}).get('ground', 'TBA'),
                                'City': match_info.get('venueInfo', {}).get('city', 'TBA'),
                                'Status': match_info.get('status', 'Scheduled'),
                                'State': match_info.get('state', 'Unknown')
                            }
                            
                            # Add match score if available
                            if 'matchScore' in match:
                                score_info = match['matchScore']
                                if 'team1Score' in score_info:
                                    team1_score = score_info['team1Score']
                                    match_dict['Team 1 Score'] = f"{team1_score.get('inngs1', {}).get('runs', 0)}/{team1_score.get('inngs1', {}).get('wickets', 0)}"
                                
                                if 'team2Score' in score_info:
                                    team2_score = score_info['team2Score']
                                    match_dict['Team 2 Score'] = f"{team2_score.get('inngs1', {}).get('runs', 0)}/{team2_score.get('inngs1', {}).get('wickets', 0)}"
                            
                            all_matches.append(match_dict)
        
        # Display matches
        if all_matches:
            df = pd.DataFrame(all_matches)
            
            # Display match count
            st.subheader(f"📊 Found {len(df)} Matches")
            
            # Filter options
            st.markdown("### 🔍 Filters")
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            
            with filter_col1:
                series_filter = st.multiselect(
                    "Filter by Series",
                    options=df['Series'].unique().tolist(),
                    default=[]
                )
            
            with filter_col2:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=df['Status'].unique().tolist(),
                    default=[]
                )
            
            with filter_col3:
                state_filter = st.multiselect(
                    "Filter by State",
                    options=df['State'].unique().tolist(),
                    default=[]
                )
            
            # Apply filters
            filtered_df = df.copy()
            if series_filter:
                filtered_df = filtered_df[filtered_df['Series'].isin(series_filter)]
            if status_filter:
                filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]
            if state_filter:
                filtered_df = filtered_df[filtered_df['State'].isin(state_filter)]
            
            st.markdown("---")
            
            # Display filtered matches
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400
            )
            
            # Export options
            st.markdown("### 📤 Export Options")
            export_col1, export_col2, export_col3, export_col4 = st.columns(4)
            
            with export_col1:
                if st.button("📥 Export to CSV"):
                    filepath = export_to_csv(filtered_df, "live_matches")
                    st.success(f"✅ Exported to: `{filepath}`")
                    api_logger.info(f"Live matches exported to CSV: {filepath}")
            
            with export_col2:
                if st.button("📊 Export for Power BI"):
                    filepath = export_for_powerbi(filtered_df, "live_matches")
                    st.success(f"✅ Exported to: `{filepath}`")
                    st.info("💡 Use this file in Power BI Desktop")
                    api_logger.info(f"Live matches exported for Power BI: {filepath}")
            
            with export_col3:
                # Download button for CSV
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name="live_matches.csv",
                    mime="text/csv"
                )
            
            with export_col4:
                st.metric("Total Matches", len(filtered_df))
            
            # Match statistics
            st.markdown("---")
            st.markdown("### 📈 Match Statistics")
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("Total Matches", len(df))
            
            with stat_col2:
                live_count = len(df[df['State'] == 'In Progress'])
                st.metric("Live Now", live_count)
            
            with stat_col3:
                completed_count = len(df[df['Status'] == 'Completed'])
                st.metric("Completed", completed_count)
            
            with stat_col4:
                upcoming_count = len(df[df['State'] == 'Preview'])
                st.metric("Upcoming", upcoming_count)
            
        else:
            st.info("ℹ️ No matches found at the moment")
            st.markdown("""
            **Possible reasons:**
            - No live matches currently
            - API returned empty data
            - Off-season period
            
            Try refreshing in a few minutes.
            """)
    else:
        st.warning("⚠️ Unable to fetch match data")
        st.error("API response format unexpected. Please check API status.")

except Exception as e:
    error_msg = f"Error fetching live matches: {str(e)}"
    api_logger.error(error_msg)
    st.error(f"❌ {error_msg}")
    
    # Log failed API call to MLflow
    tracker.log_api_call(
        endpoint="/matches/v1/live",
        response_time=0,
        status_code=500,
        data_size=0
    )
    
    # Show troubleshooting tips
    with st.expander("🔧 Troubleshooting"):
        st.markdown("""
        **Common Issues:**
        
        1. **API Key Not Configured**
           - Check `.env` file has valid `RAPIDAPI_KEY`
           - Verify key is active on RapidAPI
        
        2. **Network Issues**
           - Check internet connection
           - Verify firewall settings
        
        3. **Rate Limit Exceeded**
           - Wait a few minutes
           - Upgrade RapidAPI plan
        
        4. **API Service Down**
           - Check RapidAPI status page
           - Try again later
        """)

# Sidebar info
with st.sidebar:
    st.markdown("### 📊 Live Matches Info")
    st.info("""
    This page fetches real-time cricket match data from the Cricbuzz API.
    
    **Features:**
    - Live match scores
    - Match status updates
    - Venue information
    - Team details
    - Export functionality
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("- [MLflow Dashboard](http://localhost:5000)")
    st.markdown("- [Cricbuzz API Docs](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/)")