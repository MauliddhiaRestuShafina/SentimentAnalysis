#!/usr/bin/env python3

import html
import os
import plotly
import socket
import config
from twython import Twython
from twython import TwythonAuthError, TwythonError, TwythonRateLimitError

# twitter aplication keys
os.environ['API_KEY'] = 'iBnbpKXoe6QqgEtddULWZrtfR'
os.environ['API_SECRET'] = 'OUtn0OdYwzo6piGD9hv4jYPhaoWrIuqPXZGp4KSsI4vZgO18vz'


def chart(positive, negative):
    """Return a pie chart for specified sentiments as HTML."""

    # offline plot
    # https://plot.ly/python/pie-charts/
    # https://plot.ly/python/reference/#pie
    figure = {
        "data": [
            {
                "labels": ["positiv", "negativ"],
                "hoverinfo": "none",
                "marker": {
                    "colors": [
                        "green",
                        "red",
                    ]
                },
                "type": "pie",
                "values": [positive, negative]
            }
        ],
        "layout": {
            "showlegend": True
            }
    }
    return plotly.offline.plot(figure, output_type="div", show_link=False, link_text=False)

def get_user_timeline(screen_name, count):
    """Return list of most recent tweets posted by screen_name."""

    # ensure count is valid
    if count < 1 or count > 200:
        raise RuntimeError("invalid count")

    # ensure environment variables are set
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    if not os.environ.get("API_SECRET"):
        raise RuntimeError("API_SECRET not set")

    # get screen_name's (or @screen_name's) most recent tweets
    # https://dev.twitter.com/rest/reference/get/users/lookup
    # https://dev.twitter.com/rest/reference/get/statuses/user_timeline
    # https://github.com/ryanmcgrath/twython/blob/master/twython/endpoints.py
    try:
        twitter = Twython(os.environ.get("API_KEY"), os.environ.get("API_SECRET"))
        user = twitter.lookup_user(screen_name=screen_name.lstrip("@"))
        if user[0]["protected"]:
            return None
        tweets = twitter.get_user_timeline(screen_name=screen_name, include_rts=False, count=count, tweet_mode='extended')
        tweetsList = []
        for tweet in tweets:
            tweetText = html.unescape(tweet["full_text"].replace("\n", " "))
            tweetsList.append({'tweet': tweetText, 'time': tweet['created_at'], 'score': 0.0})
        return tweetsList
    except TwythonAuthError:
        raise RuntimeError("invalid API_KEY and/or API_SECRET") from None
    except TwythonRateLimitError:
        raise RuntimeError("you've hit a rate limit") from None
    except TwythonError:
        return None
