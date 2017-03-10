# Telegram Weather Bot
# By Sven den Hartog & Johanna de Vos
# Based on: https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# https://github.com/sixhobbits/python-telegram-tutorial/blob/master/part1/echobot.py

import json 
import requests
import time
import urllib
import spacy
from geotext import GeoText
# python3: urllib.parse.quote_plus
# python2: urllib.pathname2url
import ConfigParser

c = ConfigParser.ConfigParser(allow_no_value=True)
c.read("keys.ini")

nlp = spacy.load('en')

TGTOKEN = c.get("APIKEYS", "telegram")
OWTOKEN = c.get("APIKEYS", "openweatherapi")
URL = "https://api.telegram.org/bot{}/".format(TGTOKEN)
textcomp = [u'hello', u'how are you doing?', u'thank you', u'what is the weather in London?', u'warm cold hot temperature in London?', u'wind speed force velocity in London?']

def weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city,OWTOKEN)
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
    if (len(places.cities)>0):
        for city in places.cities:
            text = text.replace(city, "London");
        doc = nlp(text)
    score = []
    max = 0
    for i, test in enumerate(textcomp):
        sim = doc.similarity(nlp(test))
        score.append(sim)
        if sim >= score[max]:
            max = i
    print score
    response = ''

    if score[max] > 0.5:
        if max == 0:
            response += "Hi! I'm Weather Bot. You can ask me questions about the weather in a particular city. "
        elif max == 1:
            response += "I'm fine. "
        elif max == 2:
            response += "You're welcome! "
        else:
            if len(places.cities) > 0:
                for city in places.cities:
                    forecast = weather(city)
                    if max == 3:
                        sky = forecast["weather"][0]["main"].lower()
                        response += "The weather in {}: {}.".format(city, sky)
                    elif max == 4:
                        temp = int(round(forecast["main"]["temp"] - 273.15))  # temperature is in Kelvin
                        response += "The temperature in {} is {} degrees Celsius. ".format(city, temp)
                    elif max == 5:
                        wind = forecast["wind"]["speed"]
                        wind_km = wind * 3.6
                        response += "The wind speed in {} is {} meters per second. That is {} kilometers per hour.".format(city, wind, wind_km)
            else:
                response += "For what city do you want to know the weather? "
    else:
        response += "Sorry, I don't get what you're saying. "

    text = urllib.quote_plus(response) # urllib.parse.quote_plus(text) # (python3)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def main():
    last_update_id = None
    print "Start"
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            answer_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()