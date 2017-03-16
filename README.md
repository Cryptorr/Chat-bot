
### WEATHER BOT
##### By Sven den Hartog & Johanna de Vos
##### Cognitive Computational Modeling of Language and Web Interaction
##### 15 March 2017

Our bot can be found [here](https://web.telegram.org/#/im?p=@to_do4325q5_bot). You can talk to it about the weather in over 200,000 cities around the world. We'll describe the steps we took in creating the weather bot here.

1. CREATE ECHO BOT
We followed an [online tutorial](https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay) to get the bot working in a basic version. This created an 'echo bot', that just echoes whatever you say to it.

2. GET WEATHER DATA
Using the _get_json_from_url_ function that was part of the above tutorial, we can scrape data from the _OpenWeatherMap_ [API](https://openweathermap.org/api). When a request for weather information in a particular city is made to the chatbot, the following information is downloaded:

 > {u'base': u'stations',
 u'clouds': {u'all': 40},
 u'cod': 200,
 u'coord': {u'lat': 51.84, u'lon': 5.85},
 u'dt': 1489138860,
 u'id': 2750053,
 u'main': {u'humidity': 75,
  u'pressure': 1029,
  u'temp': 280.14,
  u'temp_max': 281.15,
  u'temp_min': 279.15},
 u'name': u'Nijmegen',
 u'sys': {u'country': u'NL',
  u'id': 5219,
  u'message': 0.0031,
  u'sunrise': 1489125660,
  u'sunset': 1489167200,
  u'type': 1},
 u'visibility': 10000,
 u'weather': [{u'description': u'scattered clouds',
   u'icon': u'03d',
   u'id': 802,
   u'main': u'Clouds'}],
 u'wind': {u'deg': 240, u'speed': 2.1}}

 From this, we extract the temperature (in Kelvin), the weather 'type' (e.g. sun, rain, clouds, etc.), and the wind speed.

3. PROCESS AND INTERPRET THE USER MESSAGE
For this part we used the Python libraries _spaCy_ (version 1.6) and _geotext_ (version 0.2.0). The user input was transformed into a spaCy doc object. From this doc, the city name was extracted by performing named-entity recognition with geotext.

 To interpret the user message, we compared it to six pre-defined messages:
>(1) u'hello'
>(2) u'how are you doing?'
>(3) u'thank you',
>(4) u'what is the weather in London?',
>(5) u'what is the temperature warm cold hot temperature in London?'
>(6) u'what is the wind speed force velocity in London?'

 Using _word2vec_, spaCy calculates a vector representation for each word, and then returns an average of these vectors to represent the entire input sequence. The similarity function computes the cosine similarity between the vector representing the user input, and each of the vectors representing the six pre-defined messages. The pre-defined message which scores highest in similarity to the user message, will inform the response of the weather bot.

4. REPLY
This is the bot's response to each of the six pre-defined messages:
> (1) "Hi! I'm Weather Bot. You can ask me questions about the weather in a particular city."
(2) "I'm fine."
(3) "You're welcome!"
(4) "The weather in {}: {}."
(5) "The temperature in {} is {} degrees Celsius."
(6) "The wind speed in {} is {} meters per second. That is {} kilometers per hour."

 The bot only gives any of the above responses if the cosine similarity was higher than 0.5. Otherwise, it responds: "Sorry, I don't get what you're saying."

 If the match to pre-defined statements 4, 5 or 6 was higher than 0.5, but no city name could be detected, the bot responds: "For what city do you want to know the weather?"

5. EXAMPLE
* **Sven:**
Hello Weather Bot
* **Weather Bot:**
Hi! I'm Weather Bot. You can ask me questions about the weather in a particular city.
* **Sven:**
How are you
* **Weather Bot:**
I'm fine.
* **Sven:**
What can you tell me about the weather in Nijmegen
* **Weather Bot:**
The weather in Nijmegen: mist.
* **Sven:**
And how warm is it in Amsterdam?
* **Weather Bot:**
The temperature in Amsterdam is 8 degrees Celsius.
* **Sven:**
Alright, and what about the wind speed in Maastricht?
* **Weather Bot:**
The wind speed in Maastricht is 3.1 meters per second. That is 11.16 kilometers per hour.
* **Sven:**
Thanks!
* **Weather Bot:**
You're welcome!

6. POINTS FOR IMPROVEMENT
* The recognition of city names doesn't work well when the city is not capitalized (or when everything is capitalized). This seems to be a shortcoming of the geotext library.

* The bot is currently very basic, giving six different responses only. It should be relatively easy to implement more different weather queries, or more chit-chat, by adding more pre-defined input.


> Written with [StackEdit](https://stackedit.io/).