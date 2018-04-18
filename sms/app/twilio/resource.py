"""Recieve and respond to messages via Twilio.

Users can send Simple tokens via sms via the client. The 
"""

import pprint
from flask import request
from flask_restful import Resource, reqparse
from app import web3 as network
from app import sms as twilio
from app.usr.model import User
from .responses import greeting

class Client(Resource):

    def post(self):
        """Recieve messages via Twilio."""
        User.delete_all()

        sender = request.form['From']
        
        if not User.exists(sender):
            new_user = self.create_user(sender)

            twilio.api.account.messages.create(
                to = sender,
                from_ = "+18312641420",
                body = greeting
            )

        else:
            print("User exists")
        
        return {'status': 'OK'}, 200


    def create_user(self, sender):
        # create ETH account
        user_account = network.eth.account.create(sender)
        pprint.pprint(user_account)
        private_key = "test"#user_account['privateKey']

        new_user = User(
            phone = sender,
            private = private_key
        )
        
        new_user.save_to_db()

        return new_user

