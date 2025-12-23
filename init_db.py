import sqlite3

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

with open("databases/schema.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("✅ Database initialized successfully")
