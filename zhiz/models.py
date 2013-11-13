# coding=utf8

"""
    zhiz.models
    ~~~~~~~~~~~

    zhiz's models: author, post, blog,
"""

from hashlib import md5

from zhiz import app
from zhiz.markdown import markdown

from CURD import Model, Field, Database, PrimaryKey, ForeignKey


class Author(Model):

    name = Field()
    email = Field()
    description = Field()
    url = Field()

    @property
    def gravatar_id(self):
        return md5(self.email).hexdigest()


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

    @property
    def summary(self):
        return markdown.render(self.body[:150])


class Admin(Model):

    passwd = Field()


Database.config(**app.config['DB_CFG'])
