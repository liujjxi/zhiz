# coding=utf8

from flask import render_template, request

from zhiz import app
from zhiz.models import *


@app.route('/')
def index():
    return app.config["DB_CFG"]["db"]
