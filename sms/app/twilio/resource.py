# -*- encoding: utf-8 -*-

"""Recieve and respond to messages via Twilio.

Users can send Simple tokens via sms via the client. The 
"""


import re
import pprint
import string
from flask import request
from flask_restful import Resource, reqparse
from app import web3 as network
from app import sms as twilio
from app.usr.model import User
import app.twilio.responses as responses


class Client(Resource):

    sender = ''
    send_message = ''

    def post(self):
        """Recieve messages via Twilio."""
        #User.delete_all()

        self.sender = request.form['From']
        self.sender_message = request.form['Body']

 
        
