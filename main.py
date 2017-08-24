# -*- coding: utf-8 -*-
# @Author: Rishabh Thukral
# @Date:   2017-08-23 02:40:32
# @Last Modified by:   Rishabh Thukral
# @Last Modified time: 2017-08-24 08:15:52

import logging
from flask import Flask

app = Flask(__name__)

from web.views import main


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


#registering the blueprint declared in web.views
app.register_blueprint(main, url_prefix='/') 

if __name__ == "__main__":
    
    app.run()

