# coding=utf8

"""
    zhiz.models
    ~~~~~~~~~~~

    zhiz's models: author, post, blog,
"""

from zhiz import app

from CURD import Model, Field, Database, PrimaryKey, ForeignKey


class Author(Model):

    name = Field()
    email = Field()
    description = Field()
    url = Field()


class Blog(Model):

    name = Field()
    description = Field()
    disqus = Field()


class Post(Model):

    datetime = Field()
    title = Field()
    title_pic = Field()
    body = Field()
    published = Field()


class Admin(Model):

    passwd = Field()


Database.config(**app.config['DB_CFG'])
