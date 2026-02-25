import streamlit as st
from utils.logger import app_logger

st.set_page_config(page_title="Home - Cricbuzz LiveStats", page_icon="🏠", layout="wide")

app_logger.info("Home page accessed")

st.title("🏠 Home - Cricbuzz LiveStats")

st.markdown("""
## Welcome to Cricbuzz LiveStats!

A comprehensive cricket analytics dashboard combining real-time API data with SQL-based analytics.

---

### 🎯 Project Overview

**Cricbuzz LiveStats** is a production-grade sports analytics platform that demonstrates:

- **Real-time Data Integration**: Live match updates from Cricbuzz API
- **Database Management**: MySQL with normalized schema across 6 tables
- **Advanced Analytics**: 25+ SQL queries from beginner to expert level
- **Performance Monitoring**: MLflow tracking for APIs, queries, and data quality
- **Cloud Deployment**: Docker containerization and AWS deployment scripts
- **Business Intelligence**: Power BI integration for executive dashboards

---

### 📊 Features

#### 1. Live Match Tracking 🏏
- Real-time scorecards with ball-by-ball updates
- Team lineups and player information
- Match status, venue details, and conditions
- Export functionality for further analysis

#### 2. Player Statistics ⭐
- Top run scorers across all formats
- Leading wicket-takers and economy rates
- Career batting and bowling averages
- Format-wise performance comparison

#### 3. SQL Analytics Dashboard 📈
**Beginner Queries (8)**:
- Basic player filtering and sorting
- Simple aggregations and grouping
- Recent matches and high scores

**Intermediate Queries (8)**:
- Multi-table JOINs
- Complex aggregations
- Partnership analysis
- Home vs Away performance

**Advanced Queries (9)**:
- Window functions
- Statistical calculations
- Performance rankings
- Trend analysis with CTEs

#### 4. CRUD Operations ✏️
- Create: Add new players to database
- Read: View and search all players
- Update: Modify player information
- Delete: Remove players from database

#### 5. MLflow Integration 🔬
Tracks:
- API call performance (response time, status codes)
- SQL query execution times
- Data quality metrics (null %, duplicates)
- System performance over time

#### 6. Data Export 📤
- CSV export for data analysis
- Excel export with formatting
- Power BI integration files
- Automated report generation

---

### 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit 1.31 |
| **Backend** | Python 3.11 |
| **Database** | MySQL 8.0 |
| **API** | Cricbuzz (RapidAPI) |
| **Monitoring** | MLflow 2.9 |
| **Containerization** | Docker + Docker Compose |
| **Cloud** | AWS (EC2, S3, CloudWatch) |
| **BI Tool** | Power BI Desktop |
            """)