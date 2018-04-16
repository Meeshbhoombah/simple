"""Recieve and respond to messages via Twilio.

Users can send Simple tokens via sms via the client. The 

"""

import pprint
from flask_restful import Resource, reqparse

class Client(Resource):

    def post(self):
        """Recieve messages via Twilio."""
        parser = reqparse.RequestParser()
        parser.add_argument('form', help = 'This field cannot be blank', required = True)

        data = parser.parse_args()
        pprint.pprint(data)

        return {'status': 'OK'}, 200

