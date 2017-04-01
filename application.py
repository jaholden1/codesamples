from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *
import time

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

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """Show users stocks on homepage"""
    
    # query database for stocks
    rows = db.execute("SELECT stock, name, sum(shares)shares, price FROM stocks WHERE user_id = :id and status='BOUGHT' group by stock", id=session["user_id"])
    stocks = []
    # iterate through each result and lookup current price of Stock
    for row in rows:
        quote = lookup(row["stock"])
        total = quote["price"] * row["shares"]
    # save updated values in Dict to pass to index.html
        DICT = {"stock": row["stock"], "name": row["name"], "shares": row["shares"], "price": '${:,.2f}'.format(quote["price"]), "total": '${:,.2f}'.format(total)}    
        stocks.append(DICT)
    # query database for user cash value
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    return render_template("index.html",stocks=stocks, cash='${:,.2f}'.format(cash[0]["cash"]))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # can user afford the stock?
        result = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = result[0]["cash"]
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must provide valid number of shares")        
        # validate inputs
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        elif not request.form.get("shares") or int(request.form.get("shares")) < 1:
            return apology("must provide valid number of shares")

        
        # find current value    
        quote = lookup(request.form.get("symbol"))
        if not quote:
           return apology("Stock option does not exist")  
           
        #calculate current price by shares
        cost = float(quote["price"]) * float(request.form.get("shares"))
        if cash < cost:
            return apology("Cannot afford stock")

        ## add foreign key and indexes to table purchases
        # insert into database
        query = db.execute("INSERT INTO stocks(user_id, stock, shares, price, name) values (:id, :symbol, :shares, :price, :name)", id=session["user_id"], symbol=request.form.get("symbol"), shares=request.form.get("shares"), price=quote["price"], name=quote["name"]) 
        if not query:
            return apology("oh oh. Something went wrong")
            
        # update user cash value
        cashLeft = cash - cost
        updateCash = db.execute("UPDATE users SET cash = :cashLeft where id = :id", cashLeft=cashLeft, id=session["user_id"])
    
        # redirect user to home page
        return redirect(url_for("index"))
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    # query all stocks exchanges for user
    rows = db.execute("SELECT * FROM stocks WHERE user_id = :id", id=session["user_id"])
    stocks = []
    if not rows:
            return apology("oh oh. Something went wrong")
    for row in rows:
        DICT = {"stock": row["stock"], "name": row["name"], "shares": row["shares"], "price": '${:,.2f}'.format(row["price"]), "date": row["date"], "status": row["status"]}    
        stocks.append(DICT)
    return render_template("history.html", stocks=stocks )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # lookup quote
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Quote not found")
            
        # display quote
        return render_template("quoteresult.html", name=quote["name"], price='${:,.2f}'.format(quote["price"]), symbol=quote["symbol"])
        
        # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("password and confirmation do not match")
        hashPass = pwd_context.encrypt(request.form.get("password"))
        
        # insert user to database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hashPass)
        # verify doesn't already exist
        if not result:
            return apology("user already exists")
        
        # save userid
        userId = db.execute("SELECT id FROM users WHERE username = :username and hash=:password", username=request.form.get("username"), password=hashPass)
        # remember which user has logged in
        session["user_id"] = userId[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    ## stock is sold at current price
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if request.form.get("stockOptions") == "":
            return apology("must provide symbol")
        #try:
        queryCash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        querySale = db.execute("SELECT stock, sum(shares)shares FROM stocks WHERE stock = :stock and status=:status and user_id=:id", stock=request.form.get("stockOptions"), status="BOUGHT", id=session["user_id"])
        quote = lookup(querySale[0]["stock"])
        cash = (quote["price"] * querySale[0]["shares"]) + queryCash[0]["cash"]
        updateCash = db.execute("UPDATE users SET cash=:cash where id = :id", cash=cash, id=session["user_id"])
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        query = db.execute("UPDATE stocks SET status=:status, date=:date where stock = :stock and user_id=:id", status="SOLD", date=date, stock=request.form.get("stockOptions"), id=session["user_id"])
        #except:
            #return apology("oh oh. Something went wrong")
            
        # redirect user to home page
        return redirect(url_for("index"))
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        result = db.execute("SELECT DISTINCT stock FROM stocks  WHERE user_id = :id and status=:status", id=session["user_id"], status="BOUGHT")
        return render_template("sell.html", stocks=result)
           
    
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Update password."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure password entered
        if not request.form.get("password"):
            return apology("must provide new password")
            
        # ensure password matches confirm password
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("password and confirmation do not match")
            
        hashPass = pwd_context.encrypt(request.form.get("password"))
        # update password
        rows = db.execute("UPDATE users set  hash = :hash WHERE id = :id", hash=hashPass, id=session["user_id"])

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("profile.html")

