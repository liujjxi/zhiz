# coding=utf8

from flask import render_template, request

from zhiz import app
from zhiz.models import *


@app.route('/')
def index():
    return app.config["DB_CFG"]["db"]


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
