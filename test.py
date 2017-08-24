# -*- coding: utf-8 -*-
# @Author: Rishabh Thukral
# @Date:   2017-08-24 21:46:49
# @Last Modified by:   Rishabh Thukral
# @Last Modified time: 2017-08-24 21:54:26

from flask import Flask, render_template, flash, redirect, url_for
app = Flask(__name__)

@app.route('/tweets/<username>')
def get_tweets(username):
	flash ("you are logged in as " + username)

	tweets = []
	return render_template("tweets.html", tweets = tweets)

@app.route('/logout')
def logout():
    # session.pop('logged_in', None)
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

if __name__ == '__main__':
	app.run(debug=True)