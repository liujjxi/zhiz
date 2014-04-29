# coding=utf8

"""
    zhiz.utils
    ~~~~~~~~~~

    util functions:

      flashx.success(message)
      flashx.warning(message)
      flashx.error(message)
"""


from flask import flash


class flashx(object):

    @staticmethod
    def success(message):
        return flash(dict(type='success', content=message))

    @staticmethod
    def warning(message):
        return flash(dict(type='warning', content=message))

    @staticmethod
    def error(message):
        return flash(dict(type='error', content=message))
