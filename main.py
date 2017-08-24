# -*- coding: utf-8 -*-
# @Author: Rishabh Thukral
# @Date:   2017-08-23 02:40:32
# @Last Modified by:   Rishabh Thukral
# @Last Modified time: 2017-08-24 23:48:51

import logging
from flask import Flask, Blueprint, render_template, session, request, redirect, flash, url_for
from flask_restful import Api, reqparse, Resource
from urllib.parse import parse_qsl
import oauth2 as oauth
from functools import wraps
import json
import os

app = Flask(__name__)
api = Api(app)

app.secret_key = "pOTCgqJXxNZnZh7F5U2IoGxuaMvThulG"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Tweet

engine = create_engine("postgres+psycopg2://aws_postgres:root1234@postgres-instance.cuxzbqqougwh.us-west-2.rds.amazonaws.com:5432/twitub")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

# from web.views import main, session
# from twitub.resources import callbackResource


consumer_key = "Gz5PF7GzHw6qaYZYQOLxP8Vt8"
consumer_secret = "p2FAnTBhNDHxYsdvbYaIZWh3YD3AnpGrzCrbmylG0ZNlnvtVaa"

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'

consumer = oauth.Consumer(consumer_key, consumer_secret)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

#registering the blueprint declared in web.views
# app.register_blueprint(main, url_prefix='/')

class callbackResource(Resource):
	def get(self):
		recievedArguments = requestArguments1.parse_args()
		print (recievedArguments)
		request_token = {}
		request_token['oauth_token'] = recievedArguments['oauth_token']
		oauth_verifier = recievedArguments['oauth_verifier']
		user = dbsession.query(User).filter(User.access_token == request_token['oauth_token']).one()

		request_token['oauth_token_secret'] = user.access_token_secret

		token = oauth.Token(request_token['oauth_token'],
    		request_token['oauth_token_secret'])
		token.set_verifier(oauth_verifier)

		client = oauth.Client(consumer, token)

		resp, content = client.request(access_token_url, "POST")
		access_token = dict(parse_qsl(content))

		print (access_token)
		if access_token:

			_ = dbsession.query(User).filter(User.twitter_user_id == access_token[b'user_id'].decode('utf-8'))
			
			if _.one_or_none() != None :
				_ = _.one()
				_.access_token = access_token[b'oauth_token'].decode('utf-8')
				_.access_token_secret = access_token[b'oauth_token_secret'].decode('utf-8')
				_.new_user = False
				dbsession.add(_)
				dbsession.delete(user)

			else:
				_ = User()
				_.access_token = access_token[b'oauth_token'].decode('utf-8')
				_.access_token_secret = access_token[b'oauth_token_secret'].decode('utf-8')
				_.twitter_user_id = access_token[b'user_id'].decode('utf-8')
				_.twitter_username = access_token[b'screen_name'].decode('utf-8') 
				dbsession.add(_)

			dbsession.commit()

			session["logged_in"] = True
			
			return redirect(url_for("get_tweets", username = _.twitter_username))
		else :
			return "Twitter could not respond respond"


api.add_resource(callbackResource, "/v1/callback")
requestArguments1 = reqparse.RequestParser(bundle_errors = True)
requestArguments1.add_argument("oauth_token", type = str, location = "args")
requestArguments1.add_argument("oauth_verifier", type = str, location = "args")


def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for("index"))

	return wrap

# main = Blueprint('main', __name__,
# 	template_folder = '../templates',
# 	static_folder = '../static')

#declaring route for '/' endpoint

@app.route('/tweets/<username>', methods = ['GET', 'POST'])
@login_required
def get_tweets(username):
	flash ("you are logged in as " + username)
	try:
		user = dbsession.query(User).filter(User.twitter_username == username).one()
		
	except Exception as e:
		user = None
		flash('No user found' + username)
		return redirect(url_for('index'))
	tweets = dbsession.query(Tweet).filter(Tweet.user_id == user.id).all()
	if len(tweets) == 0:
		flash("No tweets were found right now in our database. Updation of tweets may take some time.")
	
	return render_template("tweets-new.html", tweets = tweets)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for("index"))

@app.route('/', methods = ['GET', 'POST'])
def index():
	# return 
	if request.method == 'POST':
		consumer = oauth.Consumer(consumer_key, consumer_secret)
		client = oauth.Client(consumer)

		resp, content = client.request(request_token_url, "GET")
		if resp['status'] != '200':
		    raise Exception("Invalid response %s." % resp['status'])

		request_token = dict(parse_qsl(content))
		print (request_token)
		new_user = User(access_token = request_token[b'oauth_token'].decode('utf-8'), access_token_secret = request_token[b'oauth_token_secret'].decode('utf-8'))
		dbsession.add(new_user)
		dbsession.commit()


		s = request_token[b'oauth_token']
		
		return redirect("%s?oauth_token=%s" % (authorize_url, s.decode('utf-8')))
	else:
		return render_template("index.html")
 

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)

