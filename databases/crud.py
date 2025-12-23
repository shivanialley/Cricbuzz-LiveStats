from database.db_connection import get_connection

def add_player(player):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO players VALUES (?, ?, ?, ?, ?, ?)",
        player
    )
    conn.commit()


def get_players():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM players")
    return cur.fetchall()


def delete_player(player_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM players WHERE player_id = ?", (player_id,))
    conn.commit()
