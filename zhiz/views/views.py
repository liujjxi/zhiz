# coding=utf8

from CURD import Models
from flask import render_template, abort

from zhiz import app
from zhiz.models import *
from zhiz.markdown import markdown
from zhiz.views.login import logged_in


@app.route('/')
def index():
    return page(1)


@app.errorhandler(404)
def page_not_found(error):
    blog = Blog.getone()
    author = Author.getone()
    return render_template('404.html', blog=blog, author=author), 404


def render_public(template, **data):
    models = Models(Blog, Author)
    blog, author = models.getone()
    return render_template(template, blog=blog, author=author, logged_in=logged_in(),
                           **data)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.at(post_id).getone()
    if post is None:
        abort(404)
    setattr(post, 'html', markdown.render(post.body))
    return render_public('post.html', post=post)


@app.route('/page/<int:page_number>')
def page(page_number):
    if page_number <= 0:
        abort(404)

    n = 9

    query = Post.where(published=1).orderby(
        Post.datetime, desc=True).limit(n, offset=n * (page_number-1)).select()
    results = query.execute()
    count = results.count

    if not count: # no posts
        abort(404)

    total_count = Post.select(Post.id).execute().count

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
