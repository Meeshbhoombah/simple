"""Recieve and respond to user texts via Twilio.
"""

from flask_restful import Resource, reqparse
from models import User

class Chat(Resource):

    def post(self):
        """Recieve message from Twilio and act accordingly"""
        

