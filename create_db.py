import sqlite3

conn = sqlite3.connect("database.db")

cur = conn.cursor()

cur.execute("""
CREATE TABLE vaccination(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
vaccine TEXT
)
""")

conn.commit()
conn.close()