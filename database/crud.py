from database.db_connection import get_connection
from utils.logger import app_logger

def add_player(player):
    """
    Add a new player to the database
    
    Args:
        player: Tuple of (player_id, full_name, country, role, batting_style, bowling_style)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO players (player_id, full_name, country, role, batting_style, bowling_style)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, player)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        app_logger.info(f"Player added successfully: {player[1]}")
        
    except Exception as e:
        app_logger.error(f"Error adding player: {str(e)}")
        raise


def get_players():
    """
    Get all players from database
    
    Returns:
        List of player tuples
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM players ORDER BY player_id")
        players = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        app_logger.info(f"Retrieved {len(players)} players")
        return players
        
    except Exception as e:
        app_logger.error(f"Error fetching players: {str(e)}")
        raise


def update_player(player_id, updates):
    """
    Update player information
    
    Args:
        player_id: ID of player to update
        updates: Dictionary of field: value pairs to update
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build UPDATE query dynamically
        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"UPDATE players SET {set_clause} WHERE player_id = %s"
        
        values = list(updates.values()) + [player_id]
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        app_logger.info(f"Player {player_id} updated successfully")
        
    except Exception as e:
        app_logger.error(f"Error updating player: {str(e)}")
        raise


def delete_player(player_id):
    """
    Delete a player from database
    
    Args:
        player_id: ID of player to delete
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM players WHERE player_id = %s", (player_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        app_logger.info(f"Player {player_id} deleted successfully")
        
    except Exception as e:
        app_logger.error(f"Error deleting player: {str(e)}")
        raise


def get_player_by_id(player_id):
    """
    Get specific player by ID
    
    Args:
        player_id: ID of player to retrieve
    
    Returns:
        Player tuple or None if not found
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM players WHERE player_id = %s", (player_id,))
        player = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return player
        
    except Exception as e:
        app_logger.error(f"Error fetching player {player_id}: {str(e)}")
        raise