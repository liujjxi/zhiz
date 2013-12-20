# coding=utf8


"""
    zhiz.views.security
    ~~~~~~~~~~~~~~~~~~~

    routes:

      password
        GET, `/security`, display password form
      update_password
        POST, `/security/update`, update password
"""

from hashlib import md5

from flask import render_template, request, redirect, url_for

from zhiz import app
from zhiz.models import Admin
from zhiz.views.login import login_required
from zhiz.utils import flashx


@app.route('/security')
@login_required
def password():
    return render_template('password.html', active_tab='password')


@app.route('/security/update', methods=['POST'])
@login_required
def update_password():
    password_now = request.form['password_now']
    password_new = request.form['password_new']
    password_new_repeat = request.form['password_new_repeat']

    if password_now and password_new and password_new_repeat:
        if password_new_repeat != password_new:
            flashx.warning('The two new passwords do not match')
        else:
            admin = Admin.getone()

            hashed_passwd_now = md5(password_now).hexdigest()

            if hashed_passwd_now != admin.passwd:
                flashx.warning('Incorrect password')
            else:
                admin.passwd = md5(password_new).hexdigest()
                admin.save()
                flashx.success('Save password successfully, please login again')
                return redirect(url_for('logout'))
    else:
        flashx.warning('Empty input!')
    return redirect(url_for('password'))
