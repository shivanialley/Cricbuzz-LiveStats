import streamlit as st
from utils.logger import app_logger
import os
from database.db_connection import test_connection

# Page configuration
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏏 Cricbuzz LiveStats</h1>', unsafe_allow_html=True)
st.markdown("### Real-Time Cricket Analytics & SQL-Based Insights")

app_logger.info("Main app page accessed")

# Welcome message
st.markdown("---")

# Quick intro cards
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **📊 25+ SQL Queries**
    
    Advanced analytics from beginner to expert level covering player stats, match analysis, and performance trends.
    """)

with col2:
    st.success("""
    **⚡ Live Match Data**
    
    Real-time scores and updates from Cricbuzz API with detailed scorecards and player information.
    """)

with col3:
    st.warning("""
    **🔬 MLflow Tracking**
    
    Performance monitoring, experiment logging, and data quality metrics tracking.
    """)

# Quick statistics
st.markdown("---")
st.subheader("📈 Database Statistics")

col1, col2, col3, col4 = st.columns(4)

try:
    from database.db_connection import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get counts from different tables
    cursor.execute("SELECT COUNT(*) FROM players")
    player_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM matches")
    match_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM venues")
    venue_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT format) FROM batting_stats")
    format_count = cursor.fetchone()[0]
    
    conn.close()
    
    with col1:
        st.metric("👥 Total Players", player_count)
    
    with col2:
        st.metric("🏏 Total Matches", match_count)
    
    with col3:
        st.metric("🏟️ Total Venues", venue_count)
    
    with col4:
        st.metric("📋 Formats", format_count)
        
except Exception as e:
    st.error(f"⚠️ Database connection error: {str(e)}")
    st.info("Please make sure MySQL is running and database is initialized.")
    app_logger.error(f"Failed to load statistics: {str(e)}")

# Navigation guide
st.markdown("---")
st.subheader("🧭 Navigation Guide")

st.markdown("""
**Use the sidebar** (←) to navigate between different pages:

1. **🏠 Home** - Project overview, documentation, and system status
2. **🏏 Live Matches** - Real-time cricket match updates from Cricbuzz API
3. **⭐ Top Player Stats** - Best batting and bowling performances
4. **📊 SQL Analytics** - Execute 25+ analytical SQL queries
5. **✏️ CRUD Operations** - Manage player database with Create, Read, Update, Delete

### 🔗 External Services

- **MLflow UI**: [http://localhost:5000](http://localhost:5000) - View experiment logs and metrics
- **Database**: MySQL Server on port 3306
- **API**: Cricbuzz REST API via RapidAPI

### 📚 Documentation

- **README.md**: Complete setup and usage instructions
- **GitHub**: Source code and issue tracking
- **MLflow**: Performance metrics and experiment tracking
""")

# System health status
st.markdown("---")
st.subheader("🔧 System Health Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    try:
        if test_connection():
            st.success("✅ **Database**: Connected")
        else:
            st.error("❌ **Database**: Disconnected")
    except:
        st.error("❌ **Database**: Connection Error")

with status_col2:
    if os.path.exists('logs/app.log'):
        st.success("✅ **Logging**: Active")
        # Show last log entry
        try:
            with open('logs/app.log', 'r') as f:
                lines = f.readlines()
                if lines:
                    st.caption(f"Last log: {lines[-1][:100]}...")
        except:
            pass
    else:
        st.warning("⚠️ **Logging**: Not Configured")

with status_col3:
    api_key = os.getenv('RAPIDAPI_KEY')
    if api_key and api_key != 'your_rapidapi_key_here':
        st.success("✅ **API Key**: Configured")
    else:
        st.error("❌ **API Key**: Missing")
        st.caption("Update .env file with your RapidAPI key")

# Project information
st.markdown("---")
st.subheader("📖 About This Project")

about_col1, about_col2 = st.columns(2)

with about_col1:
    st.markdown("""
    **🎯 Objective**
    
    Build a production-ready cricket analytics platform demonstrating:
    - API integration with live data sources
    - Relational database design and management
    - Advanced SQL analytics and queries
    - MLOps practices with experiment tracking
    - Cloud deployment capabilities
    
    **🛠️ Technologies**
    - **Frontend**: Streamlit
    - **Backend**: Python 3.11
    - **Database**: MySQL 8.0
    - **API**: Cricbuzz (RapidAPI)
    - **Monitoring**: MLflow
    - **Deployment**: Docker, AWS
    """)

with about_col2:
    st.markdown("""
    **📊 Features**
    - Real-time match tracking
    - Player performance analytics
    - 25 SQL queries (Beginner to Advanced)
    - CRUD operations
    - Data export (CSV, Excel, Power BI)
    - Performance monitoring
    - Cloud deployment ready
    
    **📈 Use Cases**
    - Fantasy cricket platforms
    - Sports broadcasting analytics
    - Betting odds calculation
    - Educational SQL practice
    - Data engineering portfolio
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <p style='color: #666;'>Built with ❤️ using Streamlit, MySQL, MLflow & Docker</p>
    <p style='color: #999; font-size: 0.9rem;'>
        📧 For support, check documentation or raise an issue on GitHub
    </p>
    <p style='color: #999; font-size: 0.8rem;'>Version 1.0.0 | Last Updated: January 2026</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.info("""
    **Current Setup:**
    - Database: MySQL
    - API: Cricbuzz
    - Tracking: MLflow
    - Deployment: Docker Ready
    """)
    
    if st.button("🔄 Refresh Statistics"):
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    **📚 Quick Links:**
    - [MLflow UI](http://localhost:5000)
    - [Documentation](#)
    - [GitHub Repo](#)
    """)
    
    st.markdown("---")
    st.caption("**Version:** 1.0.0")
    st.caption("**Environment:** Development")
