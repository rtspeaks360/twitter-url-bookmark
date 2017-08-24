# -*- coding: utf-8 -*-
# @Author: Rishabh Thukral
# @Date:   2017-08-24 21:58:50
# @Last Modified by:   Rishabh Thukral
# @Last Modified time: 2017-08-25 02:28:06


import tweepy
import re
from models import Base, User, Tweet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgres+psycopg2://aws_postgres:root1234@postgres-instance.cuxzbqqougwh.us-west-2.rds.amazonaws.com:5432/twitub")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

consumer_key = "Gz5PF7GzHw6qaYZYQOLxP8Vt8"
consumer_secret = "p2FAnTBhNDHxYsdvbYaIZWh3YD3AnpGrzCrbmylG0ZNlnvtVaa"

users = dbsession.query(User).filter(User.twitter_username != '').all()

while True:
	for _ in users:
		print(_.id)
		access_token = _.access_token
		access_token_secret = _.access_token_secret

		if _.last_updated_tweet_id != None:
			tweet_id = int(_.last_updated_tweet_id)
		else :
			tweet_id = 0

		auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
		auth.set_access_token(access_token,access_token_secret)

		api = tweepy.API(auth)

		public_tweets = api.home_timeline()
		x = len(public_tweets)
		try:
			for i in range(x):
				tweet = public_tweets[x - i -1]
				if tweet_id<tweet.id:
					url=tweet.text
					urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
					if(len(urls)>0):
						twt = Tweet()
						twt.twitter_id = tweet.id
						twt.tweet_text = tweet.text
						twt.embedded_url = urls[0]
						twt.twitter_contact_id = tweet.author._json['id']
						twt.contact = tweet.author._json['screen_name']
						twt.twitter_timestamp=tweet.created_at
						twt.user = _
						dbsession.add(twt)
						_.last_updated_tweet_id = public_tweets[0].id
						dbsession.add(_)
						
						try:
							dbsession.commit()
							print("added tweet")
						except e:
							print (e)
		except Exception as e:
			print(e)
			