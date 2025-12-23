-- ======================
-- PLAYERS
-- ======================
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    full_name VARCHAR(255),
    country VARCHAR(100),
    role VARCHAR(100),
    batting_style VARCHAR(100),
    bowling_style VARCHAR(100)
);

-- ======================
-- MATCHES
-- ======================
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    match_desc TEXT,
    team1 TEXT,
    team2 TEXT,
    venue_name TEXT,
    venue_city TEXT,
    match_date TEXT,
    winner TEXT,
    status TEXT,
    victory_margin INTEGER,
    victory_wickets INTEGER,
    toss_winner TEXT,
    toss_decision TEXT,
    format TEXT
);

-- ======================
-- BATTING STATS
-- ======================
CREATE TABLE IF NOT EXISTS batting_stats (
    batting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    format TEXT,
    runs INTEGER,
    balls INTEGER,
    strike_rate REAL,
    innings INTEGER,
    batting_position INTEGER,
    batting_team TEXT
);

-- ======================
-- BOWLING STATS
-- ======================
CREATE TABLE IF NOT EXISTS bowling_stats (
    bowling_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    format TEXT,
    overs REAL,
    wickets INTEGER,
    economy REAL,
    bowling_avg REAL,
    venue_id INTEGER
);

-- ======================
-- VENUES
-- ======================
CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY,
    venue_name TEXT,
    city TEXT,
    country TEXT,
    capacity INTEGER
);

-- ======================
-- SERIES
-- ======================
CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY,
    series_name TEXT,
    host_country TEXT,
    match_type TEXT,
    start_date TEXT,
    total_matches INTEGER
);
