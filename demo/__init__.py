# -*- coding: utf-8 -*-

from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('dev.cfg')

# Views setup
from demo.views import home
app.register_blueprint(home.mod)
