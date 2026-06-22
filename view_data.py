from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "vaccination_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- LOGIN PAGE ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- VIEW RECORDS ----------------
@app.route("/view")
def view():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM vaccination")
    data = cur.fetchall()
    conn.close()

    return render_template("view.html", data=data)


# ---------------- SEARCH ----------------
@app.route("/search")
def search():
    if "user" not in session:
        return redirect("/login")

    q = request.args.get("q")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM vaccination WHERE name LIKE ?",
        ('%' + q + '%',)
    )

    data = cur.fetchall()
    conn.close()

    return render_template("view.html", data=data)


# ---------------- ADD RECORD ----------------
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        vaccine = request.form["vaccine"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO vaccination(name, age, vaccine) VALUES(?,?,?)",
            (name, age, vaccine)
        )

        conn.commit()
        conn.close()

        return redirect("/view")

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)