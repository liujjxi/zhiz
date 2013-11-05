# coding=utf8

from flask import Flask


app = Flask(__name__)  # should initialize `app` first
app.config.from_pyfile('config.py')


import zhiz.views
