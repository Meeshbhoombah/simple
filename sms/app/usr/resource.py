"""Recieve and respond to user texts via Twilio.
"""

import pprint
from flask import request
from flask_restful import Resource, reqparse
from twilio.twiml.messaging_response import MessagingResponse
from .model import User

class User(Resource):

    def post(self):
        """Recieve message from Twilio and act accordingly"""
        pprint.pprint(request)

        return {'status': 'OK'}, 200


