from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///compassioneat.db")

@app.route("/")
def index():
    """homepage"""

    return render_template("index.html")
    
#@app.route("/upword", methods=["POST"])
#def upword():
#    up = upworda(request.form.get("word"))
#    if not up:
#        return redirect(url_for("index"))
    # else if user reached route via GET (as by clicking a link or via redirect)
#    else:
#        return render_template("upword.html")
@app.route("/upword", methods=["POST"])
def upword():
    down = upworda(request.form.get("word"))
    if down:
        return redirect(url_for("index"))
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("upword.html")
