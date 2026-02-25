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
from database.crud import add_player, get_players, update_player, delete_player, get_player_by_id
from utils.logger import app_logger

# Import tracker
import importlib.util
spec = importlib.util.spec_from_file_location("mlflow_tracking", os.path.join(project_root, "mlflow_custom", "mlflow_tracking.py"))
mlflow_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mlflow_module)
tracker = mlflow_module.tracker

st.set_page_config(page_title="CRUD Operations", page_icon="✏️", layout="wide")

st.title("✏️ CRUD Operations - Player Management")
st.markdown("Create, Read, Update, and Delete player records")

app_logger.info("CRUD Operations page accessed")

# Create tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["➕ Create", "📖 Read", "🔄 Update", "🗑️ Delete"])

# ============================================
# TAB 1: CREATE - Add New Player
# ============================================
with tab1:
    st.subheader("➕ Add New Player")
    st.markdown("Fill in the form below to add a new player to the database")
    
    with st.form("add_player_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            player_id = st.number_input(
                "Player ID *",
                min_value=1,
                step=1,
                help="Unique identifier for the player"
            )
            
            full_name = st.text_input(
                "Full Name *",
                placeholder="e.g., Virat Kohli",
                help="Player's full name"
            )
            
            country = st.text_input(
                "Country *",
                placeholder="e.g., India",
                help="Country the player represents"
            )
        
        with col2:
            role = st.selectbox(
                "Playing Role *",
                ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
                help="Primary playing role"
            )
            
            batting_style = st.selectbox(
                "Batting Style *",
                ["Right-hand", "Left-hand"],
                help="Batting hand preference"
            )
            
            bowling_style = st.selectbox(
                "Bowling Style *",
                ["Right-arm fast", "Left-arm fast", "Right-arm spin", "Left-arm spin", "None"],
                help="Bowling style (select 'None' for pure batsmen)"
            )
        
        st.markdown("*Required fields")
        
        submitted = st.form_submit_button("➕ Add Player", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not full_name or not country:
                st.error("❌ Please fill in all required fields")
            else:
                try:
                    # Check if player ID already exists
                    existing_player = get_player_by_id(player_id)
                    
                    if existing_player:
                        st.error(f"❌ Player ID {player_id} already exists!")
                    else:
                        # Add player to database
                        player_data = (player_id, full_name, country, role, batting_style, bowling_style)
                        add_player(player_data)
                        
                        st.success(f"✅ Player **{full_name}** added successfully!")
                        app_logger.info(f"Player added: {full_name} (ID: {player_id})")
                        
                        # Log data quality metrics
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute("SELECT COUNT(*) FROM players")
                            total_rows = cursor.fetchone()[0]
                            conn.close()
                            
                            tracker.log_data_quality(
                                table_name="players",
                                total_rows=total_rows,
                                null_count=0,
                                duplicate_count=0
                            )
                        except:
                            pass
                        
                        # Show added player info
                        st.info(f"""
                        **Added Player Details:**
                        - ID: {player_id}
                        - Name: {full_name}
                        - Country: {country}
                        - Role: {role}
                        - Batting: {batting_style}
                        - Bowling: {bowling_style}
                        """)
                        
                except Exception as e:
                    error_msg = f"Error adding player: {str(e)}"
                    app_logger.error(error_msg)
                    st.error(f"❌ {error_msg}")

# ============================================
# TAB 2: READ - View All Players
# ============================================
with tab2:
    st.subheader("📖 View All Players")
    
    # Refresh button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔄 Refresh", key="refresh_players"):
            st.rerun()
    
    try:
        # Fetch all players
        players = get_players()
        
        if players:
            # Convert to DataFrame
            df = pd.DataFrame(
                players,
                columns=['Player ID', 'Full Name', 'Country', 'Role', 'Batting Style', 'Bowling Style']
            )
            
            # Display count
            st.success(f"📊 Total Players: {len(df)}")
            
            # Search and filter options
            st.markdown("### 🔍 Search & Filter")
            search_col1, search_col2, search_col3 = st.columns(3)
            
            with search_col1:
                search_name = st.text_input("Search by Name", placeholder="Enter player name...")
            
            with search_col2:
                filter_country = st.multiselect(
                    "Filter by Country",
                    options=df['Country'].unique().tolist()
                )
            
            with search_col3:
                filter_role = st.multiselect(
                    "Filter by Role",
                    options=df['Role'].unique().tolist()
                )
            
            # Apply filters
            filtered_df = df.copy()
            
            if search_name:
                filtered_df = filtered_df[
                    filtered_df['Full Name'].str.contains(search_name, case=False, na=False)
                ]
            
            if filter_country:
                filtered_df = filtered_df[filtered_df['Country'].isin(filter_country)]
            
            if filter_role:
                filtered_df = filtered_df[filtered_df['Role'].isin(filter_role)]
            
            # Display filtered data
            st.markdown("---")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400
            )
            
            # Statistics
            st.markdown("### 📈 Statistics")
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("Total Players", len(df))
            
            with stat_col2:
                st.metric("Filtered Results", len(filtered_df))
            
            with stat_col3:
                st.metric("Countries", df['Country'].nunique())
            
            with stat_col4:
                st.metric("Roles", df['Role'].nunique())
            
            # Role distribution
            st.markdown("### 📊 Role Distribution")
            role_counts = df['Role'].value_counts()
            st.bar_chart(role_counts)
            
            app_logger.info(f"Retrieved {len(df)} players")
            
        else:
            st.info("ℹ️ No players found in database")
            st.markdown("Add players using the **Create** tab")
            
    except Exception as e:
        error_msg = f"Error fetching players: {str(e)}"
        app_logger.error(error_msg)
        st.error(f"❌ {error_msg}")

# ============================================
# TAB 3: UPDATE - Modify Player
# ============================================
with tab3:
    st.subheader("🔄 Update Player Information")
    st.markdown("Select a player and update their details")
    
    try:
        players = get_players()
        
        if players:
            # Create player selection dropdown
            player_options = {f"{p[0]}: {p[1]} ({p[2]})": p[0] for p in players}
            
            selected = st.selectbox(
                "Select Player to Update",
                list(player_options.keys())
            )
            
            selected_id = player_options[selected]
            
            # Get current player data
            current_player = get_player_by_id(selected_id)
            
            if current_player:
                st.info(f"**Current Details:** ID: {current_player[0]}, Name: {current_player[1]}, Country: {current_player[2]}")
                
                # Update form
                with st.form("update_player_form"):
                    st.markdown("**Update Fields** (leave empty to keep current value)")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input(
                            "New Full Name",
                            placeholder=current_player[1]
                        )
                        
                        new_country = st.text_input(
                            "New Country",
                            placeholder=current_player[2]
                        )
                        
                        new_role = st.selectbox(
                            "New Role",
                            ["", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
                            index=0
                        )
                    
                    with col2:
                        new_batting = st.selectbox(
                            "New Batting Style",
                            ["", "Right-hand", "Left-hand"],
                            index=0
                        )
                        
                        new_bowling = st.selectbox(
                            "New Bowling Style",
                            ["", "Right-arm fast", "Left-arm fast", "Right-arm spin", "Left-arm spin", "None"],
                            index=0
                        )
                    
                    update_submitted = st.form_submit_button("🔄 Update Player", type="primary")
                    
                    if update_submitted:
                        # Build updates dictionary
                        updates = {}
                        
                        if new_name:
                            updates['full_name'] = new_name
                        if new_country:
                            updates['country'] = new_country
                        if new_role:
                            updates['role'] = new_role
                        if new_batting:
                            updates['batting_style'] = new_batting
                        if new_bowling:
                            updates['bowling_style'] = new_bowling
                        
                        if updates:
                            try:
                                update_player(selected_id, updates)
                                st.success(f"✅ Player {selected_id} updated successfully!")
                                app_logger.info(f"Player {selected_id} updated: {updates}")
                                
                                # Show updated info
                                st.info(f"**Updated Fields:** {', '.join(updates.keys())}")
                                
                                time.sleep(1)
                                st.rerun()
                                
                            except Exception as e:
                                error_msg = f"Error updating player: {str(e)}"
                                app_logger.error(error_msg)
                                st.error(f"❌ {error_msg}")
                        else:
                            st.warning("⚠️ No fields selected for update")
        else:
            st.info("ℹ️ No players available for update")
            
    except Exception as e:
        error_msg = f"Error loading players: {str(e)}"
        app_logger.error(error_msg)
        st.error(f"❌ {error_msg}")

# ============================================
# TAB 4: DELETE - Remove Player
# ============================================
with tab4:
    st.subheader("🗑️ Delete Player")
    st.warning("⚠️ **Warning:** This action cannot be undone!")
    
    try:
        players = get_players()
        
        if players:
            # Create player selection dropdown
            player_options = {f"{p[0]}: {p[1]} ({p[2]})": p[0] for p in players}
            
            selected_delete = st.selectbox(
                "Select Player to Delete",
                list(player_options.keys()),
                key="delete_select"
            )
            
            selected_delete_id = player_options[selected_delete]
            
            # Get player details
            player_to_delete = get_player_by_id(selected_delete_id)
            
            if player_to_delete:
                # Show player details
                st.error(f"""
                **Player to be deleted:**
                - ID: {player_to_delete[0]}
                - Name: {player_to_delete[1]}
                - Country: {player_to_delete[2]}
                - Role: {player_to_delete[3]}
                """)
                
                # Confirmation checkbox
                confirm = st.checkbox(
                    f"I confirm I want to delete player {player_to_delete[1]} (ID: {player_to_delete[0]})",
                    key="delete_confirm"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(
                        "🗑️ Delete Player",
                        type="primary",
                        disabled=not confirm,
                        use_container_width=True
                    ):
                        try:
                            delete_player(selected_delete_id)
                            st.success(f"✅ Player {player_to_delete[1]} (ID: {selected_delete_id}) deleted successfully!")
                            app_logger.warning(f"Player deleted: {player_to_delete[1]} (ID: {selected_delete_id})")
                            
                            time.sleep(1)
                            st.rerun()
                            
                        except Exception as e:
                            error_msg = f"Error deleting player: {str(e)}"
                            app_logger.error(error_msg)
                            st.error(f"❌ {error_msg}")
                
                with col2:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.info("Deletion cancelled")
                
                if not confirm:
                    st.info("👆 Check the confirmation box above to enable delete button")
        else:
            st.info("ℹ️ No players available for deletion")
            
    except Exception as e:
        error_msg = f"Error loading players: {str(e)}"
        app_logger.error(error_msg)
        st.error(f"❌ {error_msg}")

# Sidebar info
with st.sidebar:
    st.markdown("### ✏️ CRUD Operations")
    st.info("""
    **Create**: Add new players
    **Read**: View all players
    **Update**: Modify player info
    **Delete**: Remove players
    
    All operations are logged and tracked for audit purposes.
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Database Info")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM players")
        player_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT country) FROM players")
        country_count = cursor.fetchone()[0]
        
        conn.close()
        
        st.success(f"""
        - Total Players: {player_count}
        - Countries: {country_count}
        """)
    except:
        st.error("Unable to fetch stats")
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Always verify before delete
    - Update only changed fields
    - Check logs for history
    - Refresh after changes
    """)