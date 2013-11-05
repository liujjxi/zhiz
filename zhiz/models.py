# coding=utf8

"""
    zhiz.models
    ~~~~~~~~~~~

    zhiz's models: author, post, blog,
"""

from zhi import app

from CURD import Model, Field, Database, PrimaryKey, ForeignKey


class Author(Model):

    name = Field()
    email = Field()
    description = Field()
    url = Field()


class Blog(Model):

    title = Field()
    description = Field()


class Post(Model):

    datatime = Field()
    title = Field()
    title_pic = Field()
    body = Field()


Database.config(**app.config['DB_CFG'])
