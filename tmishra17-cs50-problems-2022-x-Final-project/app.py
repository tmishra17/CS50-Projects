import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_results, error

app = Flask(__name__)
db = SQL("sqlite:///accounts.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

COUNTRIES = [
    "Spain",
    "United States",
    "India",
    "France",
    "United Kingdom",
    "Germany"
]

@app.route("/", methods=["GET", "POST"])
def index():
    # This part is just finance, I can just copy and paste the code I already did,
    # however I would like to implement the rest of the code they did my self, it is
    # important for my learning.

    if request.method == "POST":
        search_results = request.form.get("search")
        country = request.form.get("country")
        if country not in COUNTRIES:
            return error("Not a valid country", 403)
        country_code = {
            "Spain": "ES",
            "United States": "US",
            "India": "IN",
            "France": "FR",
            "United Kingdom": "UK",
            "Germany": "DE"
        }
        if not search_results:
            return redirect("/")
        if not country:
            return error("Please select a country", 405)
        # returns json of search results from API
        results = get_results(search_results, country_code[country])
        return render_template("results.html", results=results)
    else:

        return render_template("index.html", countries=COUNTRIES)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # Register user

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username:
            return error("Must provide username")
        elif not password or not confirm_password:
            return error("Must provide password and/or confirmation")
        elif db.execute("SELECT username FROM users WHERE username = ?", username):
            return error("Username already taken")
        elif password != confirm_password:
            return error("Both password and confirm password fields must be the same.")

        numbers = 0

        for char in password:
            if char.isnumeric():
                numbers += 1

        if numbers < 1:
            return error("Password must contain at least one number")

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hash)
        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/checkout", methods=["POST"])
def checkout():
    return render_template("checkout.html")

@app.route("/logout")
def logout():
    # Log user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")
@app.route("/contact")
def contact():
	return render_template("contact.html")


