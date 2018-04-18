"""Recieve and respond to messages via Twilio.

Users can send Simple tokens via sms via the client. The 
"""

import pprint
from flask import request
from flask_restful import Resource, reqparse
from app.usr.model import User
from responses import greeting

class Client(Resource):

    def post(self):
        """Recieve messages via Twilio."""
        # See if phonenumber exists in database
        sender = request.form['From']
        
        if not User.exists(sender):
            self.create_user(phone)
        else:
            print("User exists")

        #User.delete_all()

        return {'status': 'OK'}, 200


    def create_user(self, phone)

