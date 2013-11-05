# coding=utf8

from zhiz import app


@app.route('/')
def hello_world():
    return app.config["DB_CFG"]["db"]
