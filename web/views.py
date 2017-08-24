# -*- coding: utf-8 -*-
# @Author: Rishabh Thukral
# @Date:   2017-08-23 02:43:53
# @Last Modified by:   Rishabh Thukral
# @Last Modified time: 2017-08-23 12:19:48

from flask import Blueprint, render_template, request
import json
import oauth2 as oauth


consumer_key = "Gz5PF7GzHw6qaYZYQOLxP8Vt8"
consumer_secret = "p2FAnTBhNDHxYsdvbYaIZWh3YD3AnpGrzCrbmylG0ZNlnvtVaa"

# declaring blueprint for handling view serving activities
main = Blueprint('main', __name__,
	template_folder = '../templates',
	static_folder = '../static')


#declaring route for '/' endpoint
@main.route('/', methods = ['GET', 'POST'])
def index():
	# return 
	if request.method == 'POST':
		print "post request recieved"
		return render_template("index.html")
	else:
		return render_template("index.html")