@app.route("/view")
def view():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM vaccination")
    data = cur.fetchall()

    conn.close()

    return str(data)