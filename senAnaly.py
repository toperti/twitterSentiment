import re						# regex for cleaning up the tweets before analysis (i'm guessing that's the purpose)
import tweepy					# API that makes it easier to work with the Twitter API
from tweepy import OAuthHandler # handles OAuth Authorization
from textblob import TextBlob   # Handles the sentiment analysis

def getCreds(file):
	with open(file) as creds:
		creds = [i.rstrip() for i in creds.readlines()]
	return creds

class TwitterClient(object):
	def __init__(self):
		consumer_key, consumer_key_secret, access_token, access_token_secret = getCreds('credentials.txt')

		try:
			self.auth = OAuthHandler(consumer_key, consumer_key_secret)
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failure")

	# using regex to clean the tweet
	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_sentiment(self, tweet):  
		analysis = TextBlob(self.clean_tweet(tweet)) 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

