# test
# basic telegram bot
# https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# https://github.com/sixhobbits/python-telegram-tutorial/blob/master/part1/echobot.py

import json 
import requests
import time
import urllib
import numpy
import spacy
from geotext import GeoText
# python3: urllib.parse.quote_plus
# python2: urllib.pathname2url

nlp = spacy.load('en')

TOKEN = "287236464:AAFK-tgprVoLUfSzDl96SkxNK-w7lw77_Lg" # don't put this in your repo! (put in config, then import config)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
textcomp = [u'hello', u'how are you', u'weather in London', u'temperature in London']

def weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=385960ef90069e839464dbf900cbf5ed".format(city)
    forecast = get_json_from_url(url)
    #print forecast
    return forecast

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def answer_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    doc = nlp(text)
    places = GeoText(text)
    print places.cities
    score = []
    max = 0
    for i, test in enumerate(textcomp):
        sim = doc.similarity(nlp(test))
        score.append(sim)
        if sim >= score[max]:
            max = i
    response = textcomp[max] + ' ' + repr(score[max])
    text = urllib.pathname2url(response) # urllib.parse.quote_plus(text) # (python3)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            answer_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
