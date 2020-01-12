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
