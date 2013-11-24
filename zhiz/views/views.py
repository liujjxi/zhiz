# coding=utf8

from CURD import Models
from flask import render_template, abort, flash

from zhiz import app
from zhiz.models import *
from zhiz.markdown import markdown
from zhiz.views.login import logged_in


@app.route('/')
def index():
    return page(1)


@app.errorhandler(404)
def page_not_found(error):
    return render_public('404.html'), 404


def render_public(template, **data):
    models = Models(Blog, Author)
    query = models.select()
    results = query.execute()
    if results.count <= 0:
        flash(dict(type='warning', content='Not configure blog or author yet'))
        return render_template('error.html')
    blog, author = results.fetchone()
    return render_template(template, blog=blog, author=author, logged_in=logged_in(),
                           **data)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.at(post_id).getone()

    if post is None:
        abort(404)

    # render markdown to html
    setattr(post, 'html', markdown.render(post.body))

    # get next and prev post
    query = Post.where(Post.id._in(
        Post.where(Post.id > post_id).select(Fn.min(Post.id)),
        Post.where(Post.id < post_id).select(Fn.max(Post.id)),
    )).select(Post.id, Post.title)

    setattr(post, 'next', None)
    setattr(post, 'prev', None)

    for p in query:
        if p.id > post_id:
            post.next = p
        elif p.id < post_id:
            post.prev = p

    return render_public('post.html', post=post)


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

    total_count = Post.count()

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
