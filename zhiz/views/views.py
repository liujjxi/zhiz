# coding=utf8

from zhiz import app
from zhiz.views.utils import render_public
from zhiz.views.page import page


@app.route('/')
def index():
    return page(1)


@app.errorhandler(404)
def page_not_found(error):
    return render_public('404.html'), 404
