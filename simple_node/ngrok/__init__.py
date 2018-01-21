# -*- encoding: utf-8 -*-
"""
__init__.py

After server starts forwards port to an externally accesible ngrok URL
"""

from flask.ext.script import Manager
from flask import current_app as app

