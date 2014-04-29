# coding=utf8

from CURD import Models
from flask import render_template

from zhiz.models import Author, Blog
from zhiz.utils import flashx
from zhiz.views.login import logged_in


def render_public(template, **data):
    models = Models(Blog, Author)
    query = models.select()
    results = query.execute()

    if results.count <= 0:
        flashx.warning('Not configure blog or author yet')
        return render_template('error.html')
    blog, author = results.one()
    return render_template(template, blog=blog, author=author,
                           logged_in=logged_in(), **data)
