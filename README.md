# WEATHER BOT
# By Sven den Hartog & Johanna de Vos

Our bot can be found here: https://web.telegram.org/#/im?p=@to_do4325q5_bot
You can talk to it about the weather in over 200,000 cities around the world.

We'll now describe the steps we took in creating the weather bot

1) CREATE ECHO BOT
We followed an online tutorial to get the bot working in a basic version.
This created an 'echo bot', that just echoes whatever you say to it.
This is the link: https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay

2) GET WEATHER DATA
Using the get_json_from_url function that was part of the above tutorial,
we can scrape data from the OpenWeatherMap API.
When a request for weather information in a particular city is made to the chatbot,
the following information is downloaded:

{"coord":{"lon":5.85,"lat":51.84},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],
"base":"stations","main":{"temp":285.41,"pressure":1018,"humidity":62,"temp_min":284.15,"temp_max":286.15},
"visibility":10000,"wind":{"speed":7.7,"deg":280,"gust":12.9},"clouds":{"all":75},"dt":1489071600,"sys":{"type":1,"id":5219,
"message":0.0549,"country":"NL","sunrise":1489039366,"sunset":1489080718},"id":2750053,"name":"Nijmegen","cod":200} 

From this, we extract the temperature (in Kelvin) and the weather 'type' (e.g. sun, rain, clouds, etc.)

3) PROCESS AND INTERPRET THE USER MESSAGE
For this part we used the Python libraries spaCy (version 1.6) and geotext (version 0.2.0).
The user input was transformed into a spaCy doc object.
From this doc, the city name was extracted by performing named-entity recognition with geotext.

To interpret the user message, we compared it to four pre-defined messages:
[u'hello', u'how are you', u'weather in London', u'temperature in London']
Using word2vec, spaCy calculates a vector representation for each word, 
and then returns an average of these vectors to represent the entire input sequence.
The similarity function computes the cosine similarity between the vector representing the user input,
and each of the vectors representing the four pre-defined messages.
The pre-defined message which scores highest in similarity to the user message,
will inform the response of the weather bot.

4) REPLY
This is the bot's response to each of the four pre-defined messages:
'hello' --> "Hi! I'm Weather Bot. You can ask me questions about the weather in a particular city."
'how are you' --> "I'm fine. How are you?"
'weather in London' --> "The weather in {} is {}" (first empty space is city, second is weather type, e.g. 'sun' or 'rain')
'temperature in London' --> "The temperature in {} is {} degrees Celsius." (first empty space is city, second is temperature)

The bot only gives any of the above responses if the cosine similarity was higher than 0.5.
Otherwise, it responds: "Sorry, I don't get what you're saying."

If the match to 'weather in London' or 'temperature in London' was higher than 0.5, but no city name could be detected,
the bot responds: "For what city do you want to know the weather?"

5) EXAMPLE


6) POINTS FOR IMPROVEMENT
- The recognition of city names doesn't work well when the city is not capitalized (or when everything is capitalized).
  This seems to be a shortcoming of the geotext library.
  
- The bot is currently very basic, giving [xx] different responses only.
  It should be relatively easy to implement more different weather queries, or more chit-chat,
  by adding more pre-defined input.
