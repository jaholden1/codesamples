import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from werkzeug import secure_filename
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *
import time


# configure application
app = Flask(__name__)

# path to the upload directory
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# allowable extensions
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# for a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

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
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            #return apology("invalid username and/or password")
            return redirect(url_for("index"))

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
        result = db.execute("INSERT INTO users (username, password) VALUES (:username, :hash)", username=request.form.get("username"), hash=hashPass)
        # verify doesn't already exist
        if not result:
            # return apology("user already exists")
            return redirect(url_for("index"))
        
        # save userid
        userId = db.execute("SELECT id FROM users WHERE username = :username and password=:password", username=request.form.get("username"), password=hashPass)
        # remember which user has logged in
        session["user_id"] = userId[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/")
def index():
    """homepage"""
    # get top 5 rated recipes for homepage
    ratings = db.execute("SELECT vegan.id, ratings.recipe_id, ratings.rating, ratings.comment, recipes.name, recipes.image FROM ratings JOIN recipes ON recipes.id = ratings.recipe_id join vegan on vegan.recipe_id = recipes.id ORDER BY ratings.rating desc LIMIT 5")
    return render_template("index.html", ratings=ratings)
    
@app.route("/search", methods=["GET", "POST"])
def search():
    """Search non vegan item substitutions"""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # find non veg item in database
        nonveg = "%" + request.form.get("nonveg") + "%"
        result = db.execute("SELECT id FROM carnivore WHERE name like lower(:nonveg)", nonveg=nonveg)
        if len(result) > 0:
            nonvegid = result[0]["id"]
            
            # find all veg items in db with nonveg foreign key
            # find all without recipes
            vegresult = db.execute("SELECT id, name, recipe_id FROM vegan WHERE carn_id = :nonvegid and recipe_id is null", nonvegid=nonvegid)
            # assign variables that show/hide content on search page
            noshopping = "False"
            nocooking = "False"
            if len(vegresult) == 0:
                noshopping = "True"
            # find all with recipes
            vegresultrecipe = db.execute("SELECT vegan.id, vegan.name, vegan.recipe_id, recipes.image FROM vegan join recipes on recipes.id = vegan.recipe_id WHERE carn_id = :nonvegid and recipe_id is not null", nonvegid=nonvegid)
            if len(vegresultrecipe) == 0:
                nocooking = "True"
            return render_template("search.html", nonvegid=nonvegid, vegids=vegresult, vegidrecipes=vegresultrecipe, nonveg=nonveg, noshopping=noshopping, nocooking=nocooking)
        else:
            return apology("Sorry! No vegan substitution found!")      
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")
        

@app.route("/recipe", methods=["GET", "POST"])
def recipe():
    """Get selected vegan recipe/substitution"""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # get recipe id
        ratio = db.execute("SELECT id, recipe_id FROM vegan WHERE id = :id", id=request.form.get("recipeOptions"))
        vegid = ratio[0]["recipe_id"]
        recipeid = ratio[0]["id"]
        
        # get recipe for selected item
        result = db.execute("SELECT recipes.id, recipes.name, recipes.directions, recipes.servings,  recipes.date_submitted, recipes.image, vegan.carn_id FROM recipes left outer join vegan on vegan.recipe_id = recipes.id left outer join carnivore on carnivore.id = vegan.carn_id  WHERE recipes.id = :vegid", vegid=vegid)
        
        # designate single values for recipe
        name = result[0]["name"]
        #vegid = result[0]["id"]
        carnid = result[0]["carn_id"]
        directions = result[0]["directions"]
        image = result[0]["image"]

        # get ingredients for selected item
        ingredients = db.execute("SELECT * FROM ingredients WHERE recipe_id = :vegid", vegid=vegid)

        return render_template("recipe.html", name=name, directions=directions, image=image, ingredients=ingredients, vegid = vegid, nonvegid = carnid)
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")
        
@app.route("/rate", methods=["GET", "POST"])
def rate():
    """Rate vegan substitution"""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # save rating
        result = db.execute("INSERT into ratings (recipe_id, carn_id, rating, comment) values (:vegid, :nonvegid, :rating, :comment)", vegid=request.form.get("vegid"), nonvegid=request.form.get("nonvegid"),rating=request.form.get("rating"), comment=request.form.get("recipeComment"))
        
        if request.form.get("save"):
            # save recipe to users cookbook
            saved = db.execute("INSERT into savedrecipes (user_id, recipe_id, carn_id) values (:id, :vegid, :nonvegid)", id=session["user_id"], vegid=request.form.get("vegid"), nonvegid=request.form.get("nonvegid"))
        
        return redirect(url_for("index"))  
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")

@app.route("/cookbook")
def cookbook():
    """Show saved recipes."""
    
    # query all saved recipes for user
    rows = db.execute("SELECT distinct (recipes.id)recipeid, (vegan.id)vegid, vegan.name, vegan.category, savedrecipes.user_id,  (carnivore.name)carnname FROM vegan join recipes on recipes.id = vegan.recipe_id join savedrecipes on recipes.id=savedrecipes.recipe_id join carnivore on carnivore.id = vegan.carn_id where savedrecipes.user_id= :id", id=session["user_id"])
    
    return render_template("cookbook.html", recipes=rows)

@app.route("/add", methods=["GET", "POST"])
def add():
    """add recipe"""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # if there is no id for the recipe yet
        if session["recipeid"] == "":
            # error check user inputs
            try:
                servings = float(request.form.get("servings"))
            except:
                return apology("must provide valid number for servings") 
            if not request.form.get("name"):
                return apology("must provide name")
            if not request.form.get("substitution"):
                return apology("must provide substitution")
            # add recipe to db
            else:
                savedrecipe = db.execute("INSERT into recipes (name, directions, servings) values (lower(:name), :directions, :servings)", name=request.form.get("name"), directions=request.form.get("directions"), servings=request.form.get("servings"))  
                getrecipeid = db.execute("SELECT id from recipes where name=lower(:name) and directions=:directions and servings=:servings",name=request.form.get("name"), directions=request.form.get("directions"), servings=request.form.get("servings"))
                recipeid = getrecipeid[0]["id"]
                session["recipeid"] = recipeid
                # save image file
                file = request.files['file']
                # check if the file is one of the allowed types/extensions
                if file and allowed_file(file.filename):
                    # make the filename safe, remove unsupported chars
                    filename = str(session["recipeid"] ) + secure_filename(file.filename)
                    session["filename"] = filename
                    # move the file form the temp folder to upload folder
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    addimage = db.execute("UPDATE recipes set image = :image where id=:id", image=filename, id=session["recipeid"] )  
                # see if carn item is already in database
                try:
                    getcarnid = db.execute("SELECT id from carnivore where name =lower(:name)", name=request.form.get("substitution"))
                    carnid = getcarnid[0]["id"]
                # enter new carn in db if not found
                except:
                    newcarn = db.execute("INSERT into carnivore (name, category) values (lower(:name), :category)", name=request.form.get("substitution"), category=request.form.get("categories")) 
                    getcarnid = db.execute("SELECT id from carnivore where name=lower(:name) and category=:category",name=request.form.get("substitution"), category=request.form.get("categories"))
                    carnid = getcarnid[0]["id"]
                recipeid = getrecipeid[0]["id"]
                # add vegan item to db
                savedvegan = db.execute("INSERT into vegan (name, category, recipe_id, carn_id) values (lower(:name), :category, :recipe_id, :carn_id)", name=request.form.get("name"), category=request.form.get("categories"), recipe_id=session["recipeid"],carn_id=carnid)    
        else:
            # if ingredient name is null
            if not request.form.get("ingname") and request.form.get("done") != "True":
                return apology("must provide ingredient name")
                
            # if user is still inputting ingredients
            if request.form.get("done") != "True":
                # error check user inputs
                try:
                    amount = float(request.form.get("amount"))
                except:
                    return apology("must provide valid number for ingredient amount")      
            if not request.form.get("measurement") and request.form.get("done") != "True":
                return apology("must provide ingredient measurement")
            if request.form.get("ingname") !="" and request.form.get("done") != "True":
                # add ingredient to db
                savedvegan = db.execute("INSERT into ingredients (name, amount, measurement, state, recipe_id) values (lower(:name), :amount, lower(:measurement), lower(:state), :recipe_id)", name=request.form.get("ingname"), amount=request.form.get("amount"), measurement=request.form.get("measurement"),state=request.form.get("state"),recipe_id=session["recipeid"])  
        getrecipe = db.execute("SELECT (recipes.name)recipename, recipes.id, recipes.directions, recipes.servings, case when ingredients.name is null then 'noingredient' else ingredients.name end as ingredientname, ingredients.amount, ingredients.measurement, ingredients.state, ingredients.recipe_id from recipes left outer join ingredients on recipes.id = ingredients.recipe_id where recipes.id = :recipeid", recipeid=session["recipeid"])
        getrecipename = getrecipe[0]["recipename"]
        getrecipedirections = getrecipe[0]["directions"]
        getingredientname = getrecipe[0]["ingredientname"]

        if request.form.get("done") == "True":
             session["recipeid"] = ""
             session["filename"] = ""
             return redirect(url_for("index")) 
        else:
            return render_template("add.html", getrecipe=getrecipe, recipename = getrecipename, recipedirections = getrecipedirections, getingredientname=getingredientname, getimage = session["filename"] )
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:   
        session["recipeid"]  = ""
        session["filename"] = ""
        getrecipe = ""
        return render_template("add.html", getrecipe=getrecipe, recipename = "", sub=request.form.get("substitution"), name =request.form.get("name"),directions=request.form.get("directions"), servings=request.form.get("servings"))

    
    
