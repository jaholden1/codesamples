from flask import Flask, redirect, render_template, request, url_for
import os
import sys
import helpers
from analyzer import Analyzer
from helpers import get_user_timeline


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    """Analyze sum of user_names tweets as positive, negative, or positive."""
    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if not tweets:
        return redirect(url_for("index"))

 
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    
    # return list of most recent tweets posted by screen_name.
    tweets = get_user_timeline(screen_name, 100)
    
    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)

    positive, negative, neutral = 0.0, 0.0, 0.0
    # iterate through tokens, getting sum of pos, sum of neg, and sum of neutral
    for i in tweets:
        score = analyzer.analyze(i)
        if score > 0.0:
            positive += 1
        elif score < 0.0:
            negative += 1
        else:
            neutral += 1
            
    # generate chart
    chart = helpers.chart(positive, negative, neutral)
    
    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
