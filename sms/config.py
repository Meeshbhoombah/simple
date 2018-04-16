#!usr/bin/python3
"""Configurations for 'Simple SMS Client'.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = ''
    DBUSER = ''
    DBHOST = ''
    DBPASS = ''
    DBNAME = ''

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True
    DBUSER = 'rohan'
    DBHOST = '127.0.0.1'
    DBPASS = None
    DBNAME = 'simpledev'


class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'dev': Development,
    'prod': Production,

    'default': Development
}

