# coding=utf8

__version__ = '0.0.4'

from flask import Flask


app = Flask(__name__)  # should initialize `app` first
app.config.from_pyfile('config.py')
app.secret_key = app.config['SECRET_KEY']


from zhiz.views import *
