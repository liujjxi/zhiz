# coding=utf8

"""
    zhiz.views.admin
    ~~~~~~~~~~~~~~~~~
"""

from datetime import datetime
from hashlib import md5

from flask import render_template, request, redirect, url_for, flash,\
        abort

from zhiz import app
from zhiz.views.login import login_required
from zhiz.views.views import render_public
from zhiz.markdown import markdown
from zhiz.models import *


@app.route('/admin/')
@login_required
def admin():
    return redirect(url_for('write'))


@app.route('/admin/write')
@login_required
def write():
    return render_template('write.html', active_tab='write')


@app.route('/admin/create', methods=['POST'])
@login_required
def create():
    body = request.form['body']
    title = request.form['title']
    title_pic = request.form['title_pic']
    published = bool(int(request.form['published']))

    if not title:
        flash(dict(type='warning', content='Empty title'))
        return redirect(url_for('write'))

    post = Post.create(title=title, title_pic=title_pic, body=body,
                       datetime=datetime.now(), published=published)
    if published:
        flash(dict(type='success', content='Published successully'))
        return redirect(url_for('post', post_id=post.id))
    else:
        flash(dict(type='success', content='Saved to drafts successully'))
        return redirect(url_for('edit', post_id=post.id))  # jump to edit url


@app.route('/admin/update/<int:post_id>', methods=['POST'])
@login_required
def update_post(post_id):
    body = request.form['body']
    title = request.form['title']
    title_pic = request.form['title_pic']
    published = bool(int(request.form['published']))

    post = Post.at(post_id).getone()

    published_old = bool(int(post.published))

    if not post.published:  # only non-published posts update this field
        post.published = published

    post.body = body
    post.title = title
    post.title_pic = title_pic
    rows_affected = post.save()

    if rows_affected >= 0:
        if not published_old and published:  # published
            flash(dict(type='success', content='Published successfully'))
            return redirect(url_for('post', post_id=post.id))
        else:
            flash(dict(type='success', content='Saved successfully'))
            if post.published:
                return redirect(url_for('post', post_id=post.id))  # go to have a look

    else:
        flash(dict(type='error', content='Something wrong when updating post'))
    return redirect(url_for('edit', post_id=post.id))


@app.route('/preview', methods=['POST'])
@login_required
def preview():
    title = request.form['title']
    title_pic = request.form['title_pic']
    body = request.form['body']

    if not title:
        flash(dict(type='warning', content='Title is empty'))

    post = dict(
        title=title,
        title_pic=title_pic,
        html=markdown.render(body),
        datetime=datetime.now(),
        id=None  # !preview
    )

    return render_public('post.html', post=post)


@app.route('/admin/drafts')
@login_required
def drafts():
    query = Post.where(
        published=False
    ).orderby(Post.datetime, desc=True).select(
                Post.title, Post.datetime, Post.id
    )
    results = query.execute()
    posts = tuple(results.fetchall())
    return render_template('drafts.html', active_tab='drafts', posts=posts)


@app.route('/admin/edit/<int:post_id>')
@login_required
def edit(post_id):
    post = Post.findone(id=post_id)
    if post is None:
        flash(dict(type="error", content="Request post not found"))
        abort(404)
    return render_template('edit.html', post=post, active_tab='eidt')


@app.route('/admin/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    query = Post.at(post_id).delete()
    rows_affected = query.execute()

    if rows_affected <= 0:
        flash(dict(type="error", content="Something wrong when deleting post"))
        return redirect(url_for('edit', post_id=post_id))
    else:
        flash(dict(type="success", content="Delete post successfully"))
        return redirect(url_for('write'))


@app.route('/admin/settings')
@login_required
def settings():
    query = Blog.limit(1).select()
    result = query.execute()
    blog = result.fetchone()
    if blog is None:
        blog = dict(
            name='',
            description='',
            disqus= ''
        )
        flash(dict(type='warning', content='You have no settings, please edit and save'))
    return render_template('settings.html', active_tab='settings', blog=blog)


@app.route('/admin/settings/update', methods=['POST'])
@login_required
def update_settings():

    name = request.form['name']
    description = request.form['description']
    disqus = request.form['disqus']

    query = Blog.limit(1).select()
    result = query.execute()
    blog = result.fetchone()

    if blog is None:  # insert
        blog = Blog.create(name=name, description=description, disqus=disqus)
        flash(dict(type='success', content='Create settings successully'))
    else:  # do update
        blog.name = name
        blog.disqus = disqus
        blog.description = description
        blog.save()
        flash(dict(type='success', content='Save settings successully'))

    return redirect(url_for('settings'))


@app.route('/admin/author')
@login_required
def author():
    query = Author.limit(1).select()
    result = query.execute()
    author = result.fetchone()

    if author is None:
        author = dict(
            name='',
            email='',
            url='',
            description='',
        )
        flash(dict(type='warning', content='Please compelte author\'s information'))
    return render_template('author.html', active_tab='author', author=author)


@app.route('/admin/author/update', methods=['POST'])
@login_required
def update_author():

    name = request.form['name']
    email = request.form['email']
    url = request.form['url']
    description = request.form['description']

    query = Author.limit(1).select()
    result = query.execute()
    author = result.fetchone()

    if author is None:  # do a insert
        author = Author.create(name=name, email=email, url=url, description=description)
        flash(dict(type='success', content='Create author information successully'))
    else:  # do a save
        author.name = name
        author.email = email
        author.url = url
        author.description = description
        author.save()
        flash(dict(type='success', content='Save author information successully'))
    return redirect(url_for('author'))



@app.route('/admin/password')
@login_required
def password():
    return render_template('password.html', active_tab='password')


@app.route('/admin/password/update', methods=['POST'])
@login_required
def update_password():
    password_now = request.form['password_now']
    password_new = request.form['password_new']
    password_new_repeat = request.form['password_new_repeat']

    if password_now and password_new and password_new_repeat:
        if password_new_repeat != password_new:
            flash(dict(type='warning', content='The two new passwords do not match'))
        else:
            query = Admin.limit(1).select()
            result = query.execute()
            admin = result.fetchone()

            hashed_passwd_now = md5(password_now).hexdigest()

            if hashed_passwd_now != admin.passwd:
                flash(dict(type='warning', content='Incorrect password'))
            else:
                admin.passwd = md5(password_new).hexdigest()
                admin.save()
                flash(dict(type='success', content='Save password successully, please login again'))
                return redirect(url_for('logout'))
    else:
        flash(dict(type='warning', content='Empty input'))
    return redirect(url_for('password'))
