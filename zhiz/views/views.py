# coding=utf8

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


@app.route('/post/<int:post_id>')
def post(post_id):
    blog = Blog.getone()
    author = Author.getone()
    post = Post.at(post_id).getone()
    setattr(post, 'html', markdown.render(post.body))
    return render_template('post.html', blog=blog, post=post, author=author, logged_in=logged_in())


@app.route('/page/<int:page_number>')
def page(page_number):
    if page_number <= 0:
        abort(404)

    query = Post.limit(15, offset=15 * (page_number-1)).select()
    results = query.execute()
    count = results.count

    if not count: # no posts
        abort(404)

    posts = tuple(results.fetchall())
    page = dict(
        number=page_number,
        posts=posts
    )
    blog = Blog.getone()
    author = Author.getone()
    return render_template('page.html', blog=blog, page=page, author=author)
