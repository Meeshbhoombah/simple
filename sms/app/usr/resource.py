"""Recieve and respond to user texts via Twilio.
"""

import pprint
from flask_restful import Resource, reqparse
from twilio.twiml.messaging_response import MessagingResponse

class User(Resource):

    def post(self):
        """Recieve message from Twilio and act accordingly"""
        parser = reqparse.RequestParser()
        parser.add_argument('message', help = 'This field cannot be blank', required = True)

        data = parser.parse_args()
        pprint.pprint(data)

        return {'status': 'OK'}, 200


