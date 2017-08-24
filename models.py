# -*- coding: utf-8 -*-
# @Author: Rishabh Thukral
# @Date:   2017-08-23 18:04:13
# @Last Modified by:   Rishabh Thukral
# @Last Modified time: 2017-08-24 23:13:05

#importing dependencies
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

# declaring an object of the declarative base class.
Base = declarative_base()


#Models for application support
class User(Base):
	"""Provides the structure for users table in database."""

	__tablename__ = "users"
	id = Column(Integer, primary_key = True)
	twitter_user_id = Column(String(40))
	twitter_username = Column(String(40))
	access_token = Column(String(140), nullable = False)
	access_token_secret = Column(String(140), nullable = False)
	last_updated_tweet_id = Column(String(40))
	new_user = Column(Boolean, default = True)

	insert_time = Column(DateTime(timezone = True), nullable = False, default = func.now())
	update_time = Column(DateTime(timezone = True), nullable = False, default = func.now())

	tweets = relationship("Tweet", back_populates = "user")

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'twitter_username' : self.twitter_username,
			'access_token' : self.access_token,
			'access_token_secret' : self.access_token_secret,
			'last_updated_tweet_id' : self.last_updated_tweet_id,
			'insert_time' : self.insert_time,
			'update_time' : self.update_time
		}


class Tweet(Base):
	"""Provides the structure for the tweets table in the database."""

	__tablename__ = "tweets"
	id = Column(Integer, primary_key = True)
	twitter_id = Column(String(40))
	contact = Column(String(20), nullable = False)
	twitter_contact_id = Column(String(20))
	tweet_text = Column(String(200), nullable = False)
	embedded_url = Column(String(100), nullable = False)
	twitter_timestamp = Column(DateTime(timezone = True), nullable = False)

	insert_time = Column(DateTime(timezone = True), nullable = False, default = func.now())
	update_time = Column(DateTime(timezone = True), nullable = False, default = func.now())

	user_id = Column(Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates = "tweets")

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'contact' : self.contact,
			'tweet_text' : self.tweet_text,
			'embedded_url' : self.embedded_url,
			'twitter_timestamp' : self.twitter_timestamp,
			'insert_time' : self.insert_time,
			'update_time' : self.update_time
		}


engine = create_engine("postgres+psycopg2://aws_postgres:root1234@postgres-instance.cuxzbqqougwh.us-west-2.rds.amazonaws.com:5432/twitub")

Base.metadata.create_all(engine)