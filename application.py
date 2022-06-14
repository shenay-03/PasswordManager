import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")
#main
@app.route("/")
def display():
    list = []
    passwords = db.execute("SELECT * FROM passwords")
    for i in range(len(passwords)):
        list.append([passwords[i]["location"], passwords[i]["username"], passwords[i]["password"]])
    return render_template("main.html", symbols = list)
#failure
@app.route("/fail")
def fail():
    return render_template("fail.html")
    
#search
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        list = []
        search = request.form.get("search")
        passwords = db.execute("SELECT * FROM passwords WHERE location = ?", search)
        for i in range(len(passwords)):
            list.append([passwords[i]["location"], passwords[i]["username"], passwords[i]["password"]])
        return render_template("main.html", symbols = list)

#add and store user/pass
@app.route("/change", methods=["GET", "POST"])
def change():
    if request.method == "GET":
        return render_template("change.html")
    else:
        if request.form.get("type") == "add":
            db.execute("INSERT INTO passwords (location, username, password) VALUES (?, ?, ?)", request.form.get("change"), request.form.get("user"), request.form.get("pass") )
            return redirect("/")
        else:
            db.execute("DELETE FROM passwords WHERE location = ? AND username = ? AND password = ?", request.form.get("change"), request.form.get("user"), request.form.get("pass") )
            return redirect("/")

