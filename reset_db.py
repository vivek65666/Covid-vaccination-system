import sqlite3

conn = sqlite3.connect("new_database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE vaccination (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    vaccine TEXT
)
""")

conn.commit()
conn.close()

print("DB RESET DONE")