# coding=utf8

"""
    zhiz.views.login
    ~~~~~~~~~~~~~~~~

    Login stuff.

    routes:

      login
        GET, `/login`, display login page
      do_login
        POST, `/do_login`, do login
      logout
        GET, `/logout`, logout

    decorators:

      login_required
"""


from functools import wraps
from hashlib import md5

from flask import render_template, request, session, redirect, url_for

from zhiz import app
from zhiz.models import Admin
from zhiz.utils import *


SESSION_KEY = 'logged'


def logged_in():
    """if logged in, return True, else False"""
    return SESSION_KEY in session


@app.route('/login')
def login():
    if logged_in():
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')


@app.route('/do_login', methods=['POST'])
def do_login():
    if request.method == 'POST':
        passwd = request.form['passwd']

        if passwd:
            hashed_passwd = md5(passwd).hexdigest()  # md5(passwd)
            hashed_passwd_from_db = Admin.getone().passwd

            if hashed_passwd == hashed_passwd_from_db:
                session[SESSION_KEY] = 1
                flashx.success('Logged in successfully')
                return redirect(url_for('admin'))
            else:
                flashx.error('Incorrect password')
        else:
            flashx.warning('Empty input')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop(SESSION_KEY, None)
    return redirect(url_for('admin'))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not logged_in():
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper
