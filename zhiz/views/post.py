# coding=utf8

"""
    zhiz.views.post
    ~~~~~~~~~~~~~~~

    routes:

      post
        GET, `/post/<int:id>`, display single post
      write
        GET, `/post/write`, write a new post
      create
        POST, `/post/create`, create a new post
      update_post
        POST, `/post/update/<int:id>`, update a post
      edit
        GET, `/post/edit/<int:id>`, edit a post
      delete
        POST, `/post/delete/<int:id>`, delete a post
      preview
        POST, `/preview`, preview data with template `post.html`
      drafts
        GET, `/drafts`, list drafts
"""

from datetime import datetime

from flask import abort, render_template, request, redirect, url_for
from skylark import fn

from zhiz import app
from zhiz.markdown import markdown
from zhiz.models import Post
from zhiz.utils import flashx
from zhiz.views.utils import render_public
from zhiz.views.login import login_required


@app.route('/post/<int:id>')
def post(id):
    post = Post.at(id).getone()

    if post is None:
        abort(404)

    setattr(post, 'html', markdown.render(post.body))

    query = Post.where(Post.id._in(
        Post.where(Post.id > id).select(fn.min(Post.id)),
        Post.where(Post.id < id).select(fn.max(Post.id)),
    )).select(Post.id, Post.title)

    setattr(post, 'next', None)
    setattr(post, 'prev', None)

    for pst in query:  # execute query
        if pst.id > id:
            post.next = pst
        elif pst.id < id:
            post.prev = pst

    return render_public('post.html', post=post)


@app.route('/post/write')
@login_required
def write():
    return render_template('write.html', active_tab='write')


@app.route('/post/create', methods=['POST'])
@login_required
def create():
    body = request.form['body']
    title = request.form['title']
    title_pic = request.form['title_pic']
    published = bool(int(request.form['published']))

    if not title:
        flashx.warning('Empty title')
        return redirect(url_for('write'))

    post = Post.create(title=title, title_pic=title_pic, body=body,
                       datetime=datetime.now(), published=published)
    if published:
        flashx.success('Published successfully')
        return redirect(url_for('post', id=post.id))
    else:
        flashx.success('Saved to drafts successfully')
        return redirect(url_for('edit', id=post.id))  # jump to edit url


@app.route('/post/update/<int:id>', methods=['POST'])
@login_required
def update_post(id):
    body = request.form['body']
    title = request.form['title']
    title_pic = request.form['title_pic']
    published = bool(int(request.form['published']))

    post = Post.at(id).getone()

    published_old = bool(int(post.published))

    if not post.published:  # only non-published posts update this field
        post.published = published

    post.body = body
    post.title = title
    post.title_pic = title_pic

    rows_affected = post.save()

    if rows_affected >= 0:
        if not published_old and published:  # published
            flashx.success('Published successfully')
            return redirect(url_for('post', id=post.id))
        else:
            flashx.success('Saved successfully')
            if post.published:
                return redirect(url_for('post', id=post.id))

    else:
        flashx.error('Something wrong when updating post')
    return redirect(url_for('edit', id=post.id))


@app.route('/post/edit/<int:id>')
@login_required
def edit(id):
    post = Post.findone(id=id)

    if post is None:
        flashx.error('Request post not found')
        abort(404)
    return render_template('edit.html', post=post, active_tab='eidt')


@app.route('/post/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    query = Post.at(id).delete()
    rows_affected = query.execute()

    if rows_affected <= 0:
        flashx.error('Something wrong when deleting post')
        return redirect(url_for('edit', id=id))
    else:
        flashx.success('Delete post successfully')
        return redirect(url_for('write'))


@app.route('/preview', methods=['POST'])
@login_required
def preview():
    title = request.form['title']
    title_pic = request.form['title_pic']
    body = request.form['body']

    if not title:
        flashx.warning('Title is empty!')

    post = dict(
        title=title,
        title_pic=title_pic,
        html=markdown.render(body),
        datetime=datetime.now(),
        id=None  # !preview
    )

    return render_public('post.html', post=post)


@app.route('/drafts')
@login_required
def drafts():
    query = Post.where(
        published=False
    ).orderby(Post.datetime, desc=True).select(
        Post.title, Post.datetime, Post.id
    )
    results = query.execute()
    posts = tuple(results.all())
    return render_template('drafts.html', active_tab='drafts', posts=posts)
