# ================================
# BEGINNER LEVEL QUERIES (1–8)
# ================================

QUERY_1 = """
SELECT 
    full_name,
    role,
    batting_style,
    bowling_style
FROM players
WHERE country = 'India';
"""


QUERY_2 = """
SELECT 
    match_desc,
    team1,
    team2,
    venue_name || ', ' || venue_city AS venue,
    match_date
FROM matches
WHERE match_date >= DATE('now', '-7 days')
ORDER BY match_date DESC;
"""


QUERY_3 = """
SELECT 
    p.full_name,
    SUM(b.runs) AS total_runs,
    AVG(b.runs) AS batting_average,
    SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END) AS centuries
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
WHERE b.format = 'ODI'
GROUP BY p.full_name
ORDER BY total_runs DESC
LIMIT 10;
"""


QUERY_4 = """
SELECT 
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 25000
ORDER BY capacity DESC;
"""


QUERY_5 = """
SELECT 
    winner AS team,
    COUNT(*) AS total_wins
FROM matches
GROUP BY winner
ORDER BY total_wins DESC;
"""


QUERY_6 = """
SELECT 
    role,
    COUNT(*) AS player_count
FROM players
GROUP BY role;
"""


QUERY_7 = """
SELECT 
    format,
    MAX(runs) AS highest_score
FROM batting_stats
GROUP BY format;
"""


QUERY_8 = """
SELECT 
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024';
"""

# ================================
# INTERMEDIATE LEVEL QUERIES (9–16)
# ================================

QUERY_9 = """
SELECT 
    p.full_name,
    SUM(b.runs) AS total_runs,
    SUM(w.wickets) AS total_wickets,
    b.format
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
JOIN bowling_stats w 
    ON p.player_id = w.player_id 
   AND b.format = w.format
WHERE p.role = 'All-rounder'
GROUP BY p.full_name, b.format
HAVING total_runs > 1000 AND total_wickets > 50;
"""


QUERY_10 = """
SELECT 
    match_desc,
    team1,
    team2,
    winner,
    victory_margin,
    victory_type,
    venue_name
FROM matches
WHERE status = 'Completed'
ORDER BY match_date DESC
LIMIT 20;
"""


QUERY_11 = """
SELECT 
    p.full_name,
    SUM(CASE WHEN b.format='Test' THEN b.runs ELSE 0 END) AS test_runs,
    SUM(CASE WHEN b.format='ODI' THEN b.runs ELSE 0 END) AS odi_runs,
    SUM(CASE WHEN b.format='T20I' THEN b.runs ELSE 0 END) AS t20_runs,
    AVG(b.runs) AS overall_avg
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
GROUP BY p.full_name
HAVING COUNT(DISTINCT b.format) >= 2;
"""


QUERY_12 = """
SELECT 
    m.winner,
    CASE 
        WHEN v.country = m.team1 OR v.country = m.team2 THEN 'Home'
        ELSE 'Away'
    END AS match_type,
    COUNT(*) AS wins
FROM matches m
JOIN venues v ON m.venue_id = v.venue_id
GROUP BY m.winner, match_type;
"""


QUERY_13 = """
SELECT 
    p1.full_name AS batsman1,
    p2.full_name AS batsman2,
    (b1.runs + b2.runs) AS partnership_runs,
    b1.innings
FROM batting_stats b1
JOIN batting_stats b2 
  ON b1.match_id = b2.match_id 
 AND b1.innings = b2.innings
 AND b2.batting_position = b1.batting_position + 1
JOIN players p1 ON b1.player_id = p1.player_id
JOIN players p2 ON b2.player_id = p2.player_id
WHERE (b1.runs + b2.runs) >= 100;
"""


QUERY_14 = """
SELECT 
    p.full_name,
    v.venue_name,
    COUNT(DISTINCT w.match_id) AS matches,
    SUM(w.wickets) AS total_wickets,
    AVG(w.economy) AS avg_economy
FROM bowling_stats w
JOIN players p ON w.player_id = p.player_id
JOIN venues v ON w.venue_id = v.venue_id
WHERE w.overs >= 4
GROUP BY p.full_name, v.venue_name
HAVING matches >= 3;
"""


QUERY_15 = """
SELECT 
    p.full_name,
    AVG(b.runs) AS avg_runs,
    COUNT(*) AS close_matches,
    SUM(CASE WHEN m.winner = b.batting_team THEN 1 ELSE 0 END) AS wins
FROM matches m
JOIN batting_stats b ON m.match_id = b.match_id
JOIN players p ON b.player_id = p.player_id
WHERE (m.victory_margin < 50 OR m.victory_wickets < 5)
GROUP BY p.full_name;
"""


QUERY_16 = """
SELECT 
    p.full_name,
    strftime('%Y', m.match_date) AS year,
    AVG(b.runs) AS avg_runs,
    AVG(b.strike_rate) AS avg_sr
FROM batting_stats b
JOIN matches m ON b.match_id = m.match_id
JOIN players p ON b.player_id = p.player_id
WHERE m.match_date >= '2020-01-01'
GROUP BY p.full_name, year
HAVING COUNT(*) >= 5;
"""

# ================================
# ADVANCED LEVEL QUERIES (17–25)
# ================================

QUERY_17 = """
SELECT 
    toss_decision,
    ROUND(
        SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2
    ) AS win_percentage
FROM matches
GROUP BY toss_decision;
"""


QUERY_18 = """
SELECT 
    p.full_name,
    AVG(w.economy) AS economy,
    SUM(w.wickets) AS wickets
FROM bowling_stats w
JOIN players p ON w.player_id = p.player_id
JOIN matches m ON w.match_id = m.match_id
WHERE m.format IN ('ODI', 'T20')
GROUP BY p.full_name
HAVING COUNT(DISTINCT w.match_id) >= 10;
"""


QUERY_19 = """
SELECT 
    p.full_name,
    AVG(b.runs) AS avg_runs,
    SQRT(AVG(b.runs * b.runs) - AVG(b.runs) * AVG(b.runs)) AS consistency
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
WHERE b.balls >= 10
GROUP BY p.full_name;
"""


QUERY_20 = """
SELECT 
    p.full_name,
    SUM(CASE WHEN b.format='Test' THEN 1 ELSE 0 END) AS test_matches,
    SUM(CASE WHEN b.format='ODI' THEN 1 ELSE 0 END) AS odi_matches,
    SUM(CASE WHEN b.format='T20' THEN 1 ELSE 0 END) AS t20_matches,
    AVG(b.runs) AS avg_runs
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
GROUP BY p.full_name
HAVING COUNT(*) >= 20;
"""


QUERY_21 = """
SELECT 
    p.full_name,
    (
      (COALESCE(SUM(b.runs),0) * 0.01) +
      (COALESCE(AVG(b.runs),0) * 0.5) +
      (COALESCE(AVG(b.strike_rate),0) * 0.3) +
      (COALESCE(SUM(w.wickets),0) * 2) +
      ((50 - COALESCE(AVG(w.bowling_avg),50)) * 0.5) +
      ((6 - COALESCE(AVG(w.economy),6)) * 2)
    ) AS total_score
FROM players p
LEFT JOIN batting_stats b ON p.player_id = b.player_id
LEFT JOIN bowling_stats w ON p.player_id = w.player_id
GROUP BY p.full_name
ORDER BY total_score DESC;
"""


QUERY_22 = """
SELECT 
    team1,
    team2,
    COUNT(*) AS matches,
    SUM(CASE WHEN winner = team1 THEN 1 ELSE 0 END) AS team1_wins,
    SUM(CASE WHEN winner = team2 THEN 1 ELSE 0 END) AS team2_wins
FROM matches
WHERE match_date >= DATE('now','-3 years')
GROUP BY team1, team2
HAVING matches >= 5;
"""


QUERY_23 = """
WITH recent AS (
    SELECT 
        b.*,
        ROW_NUMBER() OVER (
            PARTITION BY b.player_id 
            ORDER BY m.match_date DESC
        ) AS rn
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
)
SELECT 
    p.full_name,
    AVG(CASE WHEN rn <= 5 THEN runs END) AS avg_last_5,
    AVG(CASE WHEN rn <= 10 THEN runs END) AS avg_last_10
FROM recent r
JOIN players p ON r.player_id = p.player_id
GROUP BY p.full_name;
"""


QUERY_24 = """
SELECT 
    p1.full_name AS player1,
    p2.full_name AS player2,
    AVG(b1.runs + b2.runs) AS avg_runs,
    MAX(b1.runs + b2.runs) AS highest
FROM batting_stats b1
JOIN batting_stats b2 
 ON b1.match_id = b2.match_id 
 AND b2.batting_position = b1.batting_position + 1
JOIN players p1 ON b1.player_id = p1.player_id
JOIN players p2 ON b2.player_id = p2.player_id
GROUP BY player1, player2
HAVING COUNT(*) >= 5;
"""


QUERY_25 = """
WITH quarterly AS (
    SELECT 
        p.full_name,
        strftime('%Y', m.match_date) || '-Q' ||
        ((CAST(strftime('%m', m.match_date) AS INTEGER) - 1) / 3 + 1) AS quarter,
        AVG(b.runs) AS avg_runs,
        AVG(b.strike_rate) AS avg_sr
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
    JOIN players p ON b.player_id = p.player_id
    GROUP BY p.full_name, quarter
)
SELECT * FROM quarterly;
"""
