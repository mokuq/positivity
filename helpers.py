import html
import plotly
# import socket

from twython import Twython
from twython import TwythonAuthError, TwythonError, TwythonRateLimitError

def chart(positive, negative, neutral):
    """Return a pie chart for specified sentiments as HTML."""

    # offline plot
    # https://plot.ly/python/pie-charts/
    # https://plot.ly/python/reference/#pie
    figure = {
        "data": [
            {
                "labels": ["positive", "negative", "neutral"],
                "hoverinfo": "none",
                "marker": {
                    "colors": [
                        "rgb(51, 255, 0)",
                        "rgb(255, 51, 0  )",
                        "rgb(255, 241, 118)"
                    ]
                },
                "type": "pie",
                "values": [positive, negative, neutral]
            }
        ],
        "layout": {
            "showlegend": True
            }
    }
    return plotly.offline.plot(figure, output_type="div", show_link=False, link_text=False)

def get_user_timeline(screen_name, count=200):
    """Return list of most recent tweets posted by screen_name."""

    # ensure count is valid
    if count < 1 or count > 200:
        raise RuntimeError("invalid count")
    # getting KEY and secret from
    import json
    with open('/home/Mokuq/positivity/creds-twitter') as f:
        credlist = json.load(f)
    API_KEY, API_SECRET = credlist['API_KEY'], credlist['API_SECRET']
    # get screen_name's most recent tweets
    # https://dev.twitter.com/rest/reference/get/users/lookup
    # https://dev.twitter.com/rest/reference/get/statuses/user_timeline
    # https://github.com/ryanmcgrath/twython/blob/master/twython/endpoints.py
    try:
        twitter = Twython(API_KEY, API_SECRET)
        # user = twitter.lookup_user(screen_name=screen_name)
        # if user[0]["protected"]:
        #     return None
        tweets = twitter.get_user_timeline(screen_name=screen_name, count=count)
        tweetlist = [html.unescape(tweet["text"].replace("\n", " ")) for tweet in tweets]
        return tweetlist
    except TwythonAuthError as e:
        raise RuntimeError("invalid API_KEY and/or API_SECRET") from None
    except TwythonRateLimitError as e:
        raise RuntimeError("you've hit a rate limit") from None
    except TwythonError as e:

        return None
