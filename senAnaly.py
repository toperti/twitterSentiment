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
		# checks to eliminate three things: @usernames, something, and URLs
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_sentiment(self, tweet):  
		analysis = TextBlob(self.clean_tweet(tweet)) 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10):
		
		tweets = []
		try:
			fetched_tweets = self.api.search(q = query, count = count)

			for tweet in fetched_tweets:
				parse_tweet = {}

				parse_tweet['text'] = tweet.text

				parse_tweet['sentiment'] = self.get_sentiment(tweet.text)

				if tweet.retweet_count > 0:
					if parse_tweet not in tweets:
						tweets.append(parse_tweet)
				else:
					tweets.append(parse_tweet)
			return tweets

		except tweepy.TweepError as e:
			print("Error: " + str(e))

	def main(self):
		api = TwitterClient()
		query = input("Search Twitter: ")
		tweets = api.get_tweets(query = query, count = 200)
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
		ztweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
		print("Positive tweets percentage: ", (100 * len(ptweets)/len(tweets), "%"))
		print("Negative tweets percentage: ", (100 * len(ntweets)/len(tweets), "%"))
		print("Neutral tweets percentage: ", (100 * len(ztweets)/len(tweets), "%"))

		for tweet in ptweets[:10]:
			print(tweet['text'])

		for tweet in ntweets[:10]:
			print(tweet['text'])

if __name__ == '__main__':
	tc = TwitterClient()
	tc.main()


