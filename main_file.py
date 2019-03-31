import speech_recognition as sr
import matplotlib.pyplot as plt
import pyttsx3 as p
from textblob import TextBlob
import tweepy

r = sr.Recognizer()
engine= p.init()
voices = engine.getProperty('voices')

# Use your api key her
c_key = 'xxxxx'     #consumer key
c_sec_key = 'xxxxxx' #consumer secret key
acc_token = 'xxxxxxxxx' # access token
acc_token_sec = 'xxxxxxxxxx' #access token secret

auth = tweepy.OAuthHandler(consumer_key=c_key, consumer_secret=c_sec_key)
auth.set_access_token(acc_token, acc_token_sec)
api = tweepy.API(auth)

def percentage(part, whole):
    return 100*float(part)/float(whole)

def know_review():
    polarity = 0
    neg = 0
    pos = 0
    neu = 0
    engine.say("what you wanted to know")
    engine.runAndWait()
    with sr.Microphone() as source:
        print('ask about what you want to know')
        searchterm = r.listen(source)
        text_twi = r.recognize_google(searchterm)
        engine.say('getting information about: {}'.format(text_twi))
        engine.runAndWait()
        searches = 200
        # Define searches this according to your requirement.
        tweets = tweepy.Cursor(api.search, q= text_twi).items(searches)
        for tweet in tweets:
            #print(tweet.text)
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity

            if (analysis.sentiment.polarity == 0):
                neu += 1
            elif(analysis.sentiment.polarity < 0.0):
                neg += 1
            elif(analysis.sentiment.polarity > 0.0):
                pos += 1
    pos = percentage(pos, searches)
    neg = percentage(neg, searches)
    neu = percentage(neu, searches)

    pos = format(pos, '.2f')
    neu = format(neu, '.2f')
    neg = format(neg, '.2f')

    if (polarity == 0):
        print('neutral')
        engine.say('neutral')
        engine.runAndWait()
    elif(polarity < 0):
        print('Negative')
        engine.say('Negative')
        engine.runAndWait()
    elif(polarity > 0):
        print('Positive')
        engine.say('positive')
        engine.runAndWait()
    print(pos,neg,neu)
    print(text_twi)
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [pos, neg, neu]
    colors = ['green', 'red', 'blue']
    plt.pie(sizes, labels = labels,colors = colors)
    plt.title('reviews')
    plt.axis('equal')
    plt.show()
know_review()
