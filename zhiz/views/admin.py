# coding=utf8

"""
    zhiz.views.admin
    ~~~~~~~~~~~~~~~~~
"""

from flask import render_template, request, redirect, url_for

from zhiz import app
from zhiz.views.login import login_required
from zhiz.models import *


@app.route('/admin/')
@login_required
def admin():
    return redirect(url_for('write'))


@app.route('/admin/write')
@login_required
def write():
    return render_template('write.html', active_tab='write')


@app.route('/admin/settings')
@login_required
def settings():
    return render_template('settings.html', active_tab='settings')


@app.route('/admin/author')
@login_required
def author():
    return render_template('author.html', active_tab='author')


@app.route('/admin/password')
@login_required
def password():
    return render_template('password.html', active_tab='password')
