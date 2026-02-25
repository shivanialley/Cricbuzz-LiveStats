import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize MySQL database with schema and sample data"""
    try:
        print("🏏 Initializing Cricbuzz Database...")
        
        # Connect to MySQL
        print("📡 Connecting to MySQL server...")
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL successfully")
        
        # Create database
        db_name = os.getenv('DB_NAME', 'cricbuzz_db')
        print(f"📦 Creating database: {db_name}")
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        cursor.execute(f"USE {db_name}")
        print(f"✅ Database '{db_name}' ready")
        
        print("🔨 Creating tables...")
        
        # Create players table
        cursor.execute("""
        CREATE TABLE players (
            player_id INT PRIMARY KEY,
            full_name VARCHAR(255),
            country VARCHAR(100),
            role VARCHAR(100),
            batting_style VARCHAR(100),
            bowling_style VARCHAR(100)
        )
        """)
        print("  ✅ Created players table")
        
        # Create venues table
        cursor.execute("""
        CREATE TABLE venues (
            venue_id INT PRIMARY KEY,
            venue_name VARCHAR(255),
            city VARCHAR(100),
            country VARCHAR(100),
            capacity INT
        )
        """)
        print("  ✅ Created venues table")
        
        # Create matches table
        cursor.execute("""
        CREATE TABLE matches (
            match_id INT PRIMARY KEY,
            match_desc TEXT,
            team1 VARCHAR(100),
            team2 VARCHAR(100),
            venue_name VARCHAR(255),
            venue_city VARCHAR(100),
            match_date VARCHAR(50),
            winner VARCHAR(100),
            status VARCHAR(50),
            victory_margin INT,
            victory_wickets INT,
            toss_winner VARCHAR(100),
            toss_decision VARCHAR(50),
            format VARCHAR(20)
        )
        """)
        print("  ✅ Created matches table")
        
        # Create batting_stats table
        cursor.execute("""
        CREATE TABLE batting_stats (
            batting_id INT PRIMARY KEY AUTO_INCREMENT,
            match_id INT,
            player_id INT,
            format VARCHAR(20),
            runs INT,
            balls INT,
            strike_rate DECIMAL(5,2),
            innings INT,
            batting_position INT,
            batting_team VARCHAR(100),
            FOREIGN KEY (player_id) REFERENCES players(player_id),
            FOREIGN KEY (match_id) REFERENCES matches(match_id)
        )
        """)
        print("  ✅ Created batting_stats table")
        
        # Create bowling_stats table
        cursor.execute("""
        CREATE TABLE bowling_stats (
            bowling_id INT PRIMARY KEY AUTO_INCREMENT,
            match_id INT,
            player_id INT,
            format VARCHAR(20),
            overs DECIMAL(4,1),
            wickets INT,
            economy DECIMAL(4,2),
            bowling_avg DECIMAL(5,2),
            venue_id INT,
            FOREIGN KEY (player_id) REFERENCES players(player_id),
            FOREIGN KEY (match_id) REFERENCES matches(match_id)
        )
        """)
        print("  ✅ Created bowling_stats table")
        
        # Create series table
        cursor.execute("""
        CREATE TABLE series (
            series_id INT PRIMARY KEY,
            series_name VARCHAR(255),
            host_country VARCHAR(100),
            match_type VARCHAR(50),
            start_date VARCHAR(50),
            total_matches INT
        )
        """)
        print("  ✅ Created series table")
        
        conn.commit()
        print("\n📊 Inserting sample data...")
        
        # Insert sample players
        players_data = [
            (1, 'Virat Kohli', 'India', 'Batsman', 'Right-hand', 'None'),
            (2, 'Rohit Sharma', 'India', 'Batsman', 'Right-hand', 'None'),
            (3, 'Jasprit Bumrah', 'India', 'Bowler', 'Right-hand', 'Right-arm fast'),
            (4, 'Steve Smith', 'Australia', 'Batsman', 'Right-hand', 'Right-arm spin'),
            (5, 'Pat Cummins', 'Australia', 'Bowler', 'Right-hand', 'Right-arm fast'),
            (6, 'Joe Root', 'England', 'Batsman', 'Right-hand', 'Right-arm spin'),
            (7, 'Ben Stokes', 'England', 'All-rounder', 'Left-hand', 'Right-arm fast'),
            (8, 'Kane Williamson', 'New Zealand', 'Batsman', 'Right-hand', 'Right-arm spin'),
            (9, 'Trent Boult', 'New Zealand', 'Bowler', 'Left-hand', 'Left-arm fast'),
            (10, 'Babar Azam', 'Pakistan', 'Batsman', 'Right-hand', 'None')
        ]
        
        cursor.executemany(
            "INSERT INTO players VALUES (%s, %s, %s, %s, %s, %s)",
            players_data
        )
        print("  ✅ Inserted 10 players")
        
        # Insert sample venues
        venues_data = [
            (1, 'Wankhede Stadium', 'Mumbai', 'India', 33000),
            (2, 'Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
            (3, 'Lords Cricket Ground', 'London', 'England', 28000),
            (4, 'Eden Park', 'Auckland', 'New Zealand', 50000),
            (5, 'National Stadium', 'Karachi', 'Pakistan', 34228)
        ]
        
        cursor.executemany(
            "INSERT INTO venues VALUES (%s, %s, %s, %s, %s)",
            venues_data
        )
        print("  ✅ Inserted 5 venues")
        
        # Insert sample matches
        matches_data = [
            (1, '1st ODI', 'India', 'Australia', 'Wankhede Stadium', 'Mumbai', '2024-11-15', 'India', 'Completed', 50, None, 'India', 'bat', 'ODI'),
            (2, '1st Test', 'England', 'New Zealand', 'Lords Cricket Ground', 'London', '2024-10-20', 'England', 'Completed', None, 7, 'England', 'bowl', 'Test'),
            (3, '2nd T20I', 'Pakistan', 'Australia', 'National Stadium', 'Karachi', '2024-12-01', 'Australia', 'Completed', 15, None, 'Australia', 'bat', 'T20I')
        ]
        
        cursor.executemany(
            "INSERT INTO matches VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            matches_data
        )
        print("  ✅ Inserted 3 matches")
        
        # Insert batting stats
        batting_data = [
            (1, 1, 'ODI', 85, 70, 121.43, 1, 3, 'India'),
            (1, 2, 'ODI', 120, 95, 126.32, 1, 1, 'India'),
            (2, 6, 'Test', 150, 280, 53.57, 1, 4, 'England'),
            (3, 10, 'T20I', 45, 30, 150.00, 1, 2, 'Pakistan'),
            (1, 4, 'ODI', 95, 110, 86.36, 1, 3, 'Australia'),
            (2, 8, 'Test', 88, 195, 45.13, 1, 3, 'New Zealand'),
            (3, 4, 'T20I', 62, 38, 163.16, 1, 2, 'Australia')
        ]
        
        cursor.executemany(
            "INSERT INTO batting_stats (match_id, player_id, format, runs, balls, strike_rate, innings, batting_position, batting_team) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            batting_data
        )
        print("  ✅ Inserted 7 batting records")
        
        # Insert bowling stats
        bowling_data = [
            (1, 3, 'ODI', 10.0, 3, 4.50, 25.00, 1),
            (1, 5, 'ODI', 9.5, 2, 5.20, 30.00, 1),
            (2, 7, 'Test', 25.0, 5, 2.80, 18.00, 3),
            (2, 9, 'Test', 22.0, 4, 3.20, 22.00, 3),
            (3, 3, 'T20I', 4.0, 2, 6.50, 20.00, 5)
        ]
        
        cursor.executemany(
            "INSERT INTO bowling_stats (match_id, player_id, format, overs, wickets, economy, bowling_avg, venue_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            bowling_data
        )
        print("  ✅ Inserted 5 bowling records")
        
        # Insert series
        series_data = [
            (1, 'India vs Australia ODI Series 2024', 'India', 'ODI', '2024-11-15', 3),
            (2, 'England vs New Zealand Test Series 2024', 'England', 'Test', '2024-10-20', 2),
            (3, 'Pakistan vs Australia T20I Series 2024', 'Pakistan', 'T20I', '2024-12-01', 3)
        ]
        
        cursor.executemany(
            "INSERT INTO series VALUES (%s, %s, %s, %s, %s, %s)",
            series_data
        )
        print("  ✅ Inserted 3 series")
        
        conn.commit()
        
        # Verify tables
        print("\n📊 Verifying tables...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table_name}: {count} rows")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database initialized successfully!")
        print(f"📍 Database: {db_name}")
        print(f"📍 Host: {os.getenv('DB_HOST')}")
        print(f"📍 Port: {os.getenv('DB_PORT')}")
        
    except mysql.connector.Error as e:
        print(f"\n❌ MySQL Error: {str(e)}")
        raise
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    init_database()