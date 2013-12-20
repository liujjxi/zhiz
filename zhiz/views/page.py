# coding=utf8

"""
    zhiz.views.page
    ~~~~~~~~~~~~~~~

    routes:

      page
        GET, `page/<int:page_number>`, display a page
"""

from CURD import Fn
from flask import abort

from zhiz import app
from zhiz.models import Post
from zhiz.views.utils import render_public


@app.route('/page/<int:page_number>')
def page(page_number):
    if page_number <= 0:
        abort(404)

    n = 9

    query = Post.where(published=True).orderby(
        Post.datetime, desc=True).limit(n, offset=n * (page_number-1)).select()
    results = query.execute()
    count = results.count

    if count < 0: # no posts
        abort(404)

    query = Post.where(published=True).select(Fn.count(Post.id))
    result = query.execute()
    post = result.fetchone()
    total_count = post.count_of_id

    is_first_page = True if page_number == 1 else False
    is_last_page = True if n * page_number >= total_count else False

    posts = tuple(results.fetchall())

    page = dict(
        number=page_number,
        posts=posts,
        first=is_first_page,
        last=is_last_page
    )
    return render_public('page.html', page=page)
