#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request, url_for
import helpers
from analyzer import Analyzer

application = Flask(__name__)

@application.template_filter()
def number(value):
    return "{:.4f}".format(value)

@application.template_filter()
def time(value):
    value = value[-4:] + ' ' + value[:19]
    return value

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 200)

    # absolute paths to lists
    positives = "static/SentiWS_v18c_Positive.txt"
    negatives = "static/SentiWS_v18c_Negative.txt"
    poENG = "static/positive-words.txt"
    neENG = "static/negative-words.txt"

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives, poENG, neENG)

    # variables for counting
    positive = 0
    negative = 0

    # analyzing words and adding int to matching variable
    for tweet in tweets:

        tweet['score'] = analyzer.analyze(tweet['tweet'])

        if tweet['score'] > 0.0:
            positive += tweet['score']
        elif tweet['score'] < 0.0:
            negative -= tweet['score']

    # generate chart
    chart = helpers.chart(positive, negative)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name, tweets=tweets)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()
