-- ======================
-- PLAYERS TABLE
-- ======================
CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY,
    full_name VARCHAR(255),
    country VARCHAR(100),
    role VARCHAR(100),
    batting_style VARCHAR(100),
    bowling_style VARCHAR(100)
);

-- ======================
-- MATCHES TABLE
-- ======================
CREATE TABLE IF NOT EXISTS matches (
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
);

-- ======================
-- BATTING STATS TABLE
-- ======================
CREATE TABLE IF NOT EXISTS batting_stats (
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
);

-- ======================
-- BOWLING STATS TABLE
-- ======================
CREATE TABLE IF NOT EXISTS bowling_stats (
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
);

-- ======================
-- VENUES TABLE
-- ======================
CREATE TABLE IF NOT EXISTS venues (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT
);

-- ======================
-- SERIES TABLE
-- ======================
CREATE TABLE IF NOT EXISTS series (
    series_id INT PRIMARY KEY,
    series_name VARCHAR(255),
    host_country VARCHAR(100),
    match_type VARCHAR(50),
    start_date VARCHAR(50),
    total_matches INT
);

-- ======================
-- INSERT SAMPLE DATA
-- ======================

-- Sample Players
INSERT INTO players (player_id, full_name, country, role, batting_style, bowling_style) VALUES
(1, 'Virat Kohli', 'India', 'Batsman', 'Right-hand', 'None'),
(2, 'Rohit Sharma', 'India', 'Batsman', 'Right-hand', 'None'),
(3, 'Jasprit Bumrah', 'India', 'Bowler', 'Right-hand', 'Right-arm fast'),
(4, 'Steve Smith', 'Australia', 'Batsman', 'Right-hand', 'Right-arm spin'),
(5, 'Pat Cummins', 'Australia', 'Bowler', 'Right-hand', 'Right-arm fast'),
(6, 'Joe Root', 'England', 'Batsman', 'Right-hand', 'Right-arm spin'),
(7, 'Ben Stokes', 'England', 'All-rounder', 'Left-hand', 'Right-arm fast'),
(8, 'Kane Williamson', 'New Zealand', 'Batsman', 'Right-hand', 'Right-arm spin'),
(9, 'Trent Boult', 'New Zealand', 'Bowler', 'Left-hand', 'Left-arm fast'),
(10, 'Babar Azam', 'Pakistan', 'Batsman', 'Right-hand', 'None');

-- Sample Venues
INSERT INTO venues (venue_id, venue_name, city, country, capacity) VALUES
(1, 'Wankhede Stadium', 'Mumbai', 'India', 33000),
(2, 'Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
(3, 'Lords Cricket Ground', 'London', 'England', 28000),
(4, 'Eden Park', 'Auckland', 'New Zealand', 50000),
(5, 'National Stadium', 'Karachi', 'Pakistan', 34228);

-- Sample Matches
INSERT INTO matches (match_id, match_desc, team1, team2, venue_name, venue_city, match_date, winner, status, victory_margin, victory_wickets, toss_winner, toss_decision, format) VALUES
(1, '1st ODI', 'India', 'Australia', 'Wankhede Stadium', 'Mumbai', '2024-11-15', 'India', 'Completed', 50, NULL, 'India', 'bat', 'ODI'),
(2, '1st Test', 'England', 'New Zealand', 'Lords Cricket Ground', 'London', '2024-10-20', 'England', 'Completed', NULL, 7, 'England', 'bowl', 'Test'),
(3, '2nd T20I', 'Pakistan', 'Australia', 'National Stadium', 'Karachi', '2024-12-01', 'Australia', 'Completed', 15, NULL, 'Australia', 'bat', 'T20I');

-- Sample Batting Stats
INSERT INTO batting_stats (match_id, player_id, format, runs, balls, strike_rate, innings, batting_position, batting_team) VALUES
(1, 1, 'ODI', 85, 70, 121.43, 1, 3, 'India'),
(1, 2, 'ODI', 120, 95, 126.32, 1, 1, 'India'),
(2, 6, 'Test', 150, 280, 53.57, 1, 4, 'England'),
(3, 10, 'T20I', 45, 30, 150.00, 1, 2, 'Pakistan'),
(1, 4, 'ODI', 95, 110, 86.36, 1, 3, 'Australia'),
(2, 8, 'Test', 88, 195, 45.13, 1, 3, 'New Zealand'),
(3, 4, 'T20I', 62, 38, 163.16, 1, 2, 'Australia');

-- Sample Bowling Stats
INSERT INTO bowling_stats (match_id, player_id, format, overs, wickets, economy, bowling_avg, venue_id) VALUES
(1, 3, 'ODI', 10.0, 3, 4.50, 25.00, 1),
(1, 5, 'ODI', 9.5, 2, 5.20, 30.00, 1),
(2, 7, 'Test', 25.0, 5, 2.80, 18.00, 3),
(2, 9, 'Test', 22.0, 4, 3.20, 22.00, 3),
(3, 3, 'T20I', 4.0, 2, 6.50, 20.00, 5);

-- Sample Series
INSERT INTO series (series_id, series_name, host_country, match_type, start_date, total_matches) VALUES
(1, 'India vs Australia ODI Series 2024', 'India', 'ODI', '2024-11-15', 3),
(2, 'England vs New Zealand Test Series 2024', 'England', 'Test', '2024-10-20', 2),
(3, 'Pakistan vs Australia T20I Series 2024', 'Pakistan', 'T20I', '2024-12-01', 3);