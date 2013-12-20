# coding=utf8

"""
    zhiz.views.admin
    ~~~~~~~~~~~~~~~~~
"""

from flask import redirect, url_for

from zhiz import app
from zhiz.views.login import login_required


@app.route('/admin/')
@login_required
def admin():
    return redirect(url_for('write'))
