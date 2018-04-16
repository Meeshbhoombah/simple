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

    TWILIO_SID = '' 
    TWILIO_AUTH = ''

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    DBUSER = 'rohan'
    DBHOST = '127.0.0.1'
    DBPASS = None
    DBNAME = 'simpledev'

    TWILIO_SID = os.environ.get('TWILIO_SID_TEST')
    TWILIO_AUTH = os.environ.get('TWILIO_AUTH_TEST')


class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    TWILIO_SID = os.environ.get('TWILIO_SID')
    TWILIO_AUTH = os.environ.get('TWILIO_AUTH')


config = {
    'dev': Development,
    'prod': Production,

    'default': Development
}

