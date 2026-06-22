from flask import Flask, render_template, request, redirect, session, flash, send_file
import sqlite3
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "covid123"

DB = "new_database.db"


# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vaccination (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            vaccine TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["user"] = username
            return redirect("/dashboard")

        return "Invalid Username or Password"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# ---------------- REGISTER PAGE ----------------
@app.route("/register_page")
def register_page():

    if "user" not in session:
        return redirect("/login")

    return render_template("index.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():

    if "user" not in session:
        return redirect("/login")

    name = request.form["name"]
    age = request.form["age"]
    vaccine = request.form["vaccine"]

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO vaccination(name, age, vaccine) VALUES (?, ?, ?)",
        (name, age, vaccine)
    )

    conn.commit()
    conn.close()

    flash("Registered Successfully!")

    return redirect("/view")


# ---------------- VIEW ----------------
@app.route("/view")
def view():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM vaccination")
    data = cur.fetchall()

    conn.close()

    return render_template("view.html", data=data)


# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM vaccination WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/view")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        vaccine = request.form["vaccine"]

        cur.execute("""
            UPDATE vaccination
            SET name=?, age=?, vaccine=?
            WHERE id=?
        """, (name, age, vaccine, id))

        conn.commit()
        conn.close()

        return redirect("/view")

    cur.execute("SELECT * FROM vaccination WHERE id=?", (id,))
    data = cur.fetchone()

    conn.close()

    return render_template("edit.html", data=data)

# ---------------- SEARCH (NEW) ----------------
@app.route("/search")
def search():

    if "user" not in session:
        return redirect("/login")

    q = request.args.get("q")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM vaccination WHERE name LIKE ?", ('%' + q + '%',))
    data = cur.fetchall()

    conn.close()

    return render_template("view.html", data=data)


# ---------------- CERTIFICATE (NEW) ----------------
@app.route("/certificate/<int:id>")
def certificate(id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM vaccination WHERE id=?", (id,))
    data = cur.fetchone()

    conn.close()

    filename = f"certificate_{id}.pdf"

    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Vaccination Certificate")
    c.drawString(100, 700, f"Name: {data[1]}")
    c.drawString(100, 680, f"Age: {data[2]}")
    c.drawString(100, 660, f"Vaccine: {data[3]}")
    c.save()

    return send_file(filename, as_attachment=True)


# ---------------- STATS (NEW) ----------------
@app.route("/stats")
def stats():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM vaccination")
    total = cur.fetchone()[0]

    cur.execute("SELECT vaccine, COUNT(*) FROM vaccination GROUP BY vaccine")
    data = cur.fetchall()

    conn.close()

    return render_template("stats.html", total=total, data=data)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)