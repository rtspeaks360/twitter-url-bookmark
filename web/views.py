# -*- coding: utf-8 -*-
# @Author: Rishabh Thukral
# @Date:   2017-08-23 02:43:53
# @Last Modified by:   Rishabh Thukral
# @Last Modified time: 2017-08-23 02:50:28

from flask import Blueprint, render_template


# declaring blueprint for handling view serving activities
main = Blueprint('main', __name__,
	template_folder = '../templates',
	static_folder = '../static')


#declaring route for '/' endpoint
@main.route('/')
def index():
	# return render_template("homepage.html")
	return "Hello world!"