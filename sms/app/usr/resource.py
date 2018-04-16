"""Recieve and respond to user texts via Twilio.
"""

import pprint
from app import api
from flask_restful import Resource, reqparse
from twilio.twiml.messaging_response import MessagingResponse

parser = reqparse.RequestParser()

class Conversation(Resource):

    def post(self):
        """Recieve message from Twilio and act accordingly"""
        parser = reqparse.RequestParser()
        data = parser.parseargs()
        pprint.pprint(data)



