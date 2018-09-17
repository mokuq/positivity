from flask import Flask, redirect, render_template, request, url_for
from socket import gethostname
import nltk
import helpers
from analyzer import Analyzer
# import os
# import sys
from termcolor import colored
from yandex_translate import YandexTranslate

import json
with open('/home/Mokuq/positivity/creds-yandextranslate') as f:
    yandexcredits = json.load(f)

YANDEXTRANSLATEKEY = yandexcredits ['YANDEXTRANSLATE-KEY']

translate = YandexTranslate(YANDEXTRANSLATEKEY)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))
    # absolute paths to lists
    positives =  "/home/Mokuq/positivity/positive-words.txt" # цей рядок надає нам повну адресу файлу positive-words.txt
    negatives =  "/home/Mokuq/positivity/negative-words.txt"

    analyzer1 = Analyzer(positives, negatives)
    listoftweetsorig = helpers.get_user_timeline (screen_name, count=70)

    if not listoftweetsorig:
        return render_template("search.html", screen_name=screen_name + " was not found")

    lang=translate.detect(listoftweetsorig)


    if lang=="en":
        listoftweetstr=listoftweetsorig

    else:
        print (colored("Translating...", "yellow"))

        listoftwe=translate.translate(listoftweetsorig, lang+'-en')
        listoftweetstr=listoftwe['text']

    print (colored("Calculating...", "green"))

    pos_tweets=0
    neg_tweets = 0
    neu_tweets=0
    tokenizer = nltk.tokenize.TweetTokenizer() #for tokinizing tweet

    for tweet in listoftweetstr:

        #words_in_tweet = tweet.split() #separating a tweet for words
        words_in_tweet = tokenizer.tokenize(tweet)
        score=0
        for word in words_in_tweet:
            score = score + analyzer1.analyze(word)


            if score > 0.0:
                pos_tweets = pos_tweets+1
            elif score < 0.0:
                neg_tweets=neg_tweets+1
            else:
                neu_tweets=neu_tweets+1



    total_tweets=pos_tweets+neg_tweets+neu_tweets

    positive, negative, neutral = pos_tweets/total_tweets*100, neg_tweets/total_tweets*100, neu_tweets/total_tweets*100

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name+", language of tweets is "+lang)

if __name__ == '__main__':

    if 'liveconsole' not in gethostname():
        app.run()