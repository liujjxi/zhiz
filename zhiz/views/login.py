# coding=utf8

"""
    zhiz.views.login
    ~~~~~~~~~~~~~~~~~

    login stuff defined here.
"""

from functools import wraps
from hashlib import md5

from flask import render_template, request, session, redirect, url_for, \
        flash

from zhiz import app
from zhiz.models import *


@app.route('/login')
def login():
    if logged_in():
        # already logged in, redirect to admin
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')


@app.route('/do_login', methods=['POST'])
def do_login():
    if request.method == 'POST':
        passwd = request.form['passwd']
        hashed_passwd = md5(passwd).hexdigest()
        hashed_passwd_in_db = Admin.getone().passwd
        if hashed_passwd == hashed_passwd_in_db:
            session['loged'] = 'loged'
            flash(dict(type='success', content='Logged in successfully'))
            return redirect(url_for('admin'))
        flash(dict(type='error', content='Incorrect password'))
    return redirect(url_for('login'))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'loged' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/logout')
def logout():
    session.pop('loged', None)
    return redirect(url_for('admin'))


def logged_in():
    return 'loged' in session
