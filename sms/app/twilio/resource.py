"""Recieve and respond to messages via Twilio.

Users can send Simple tokens via sms via the client. The 
"""

import pprint
from flask import request
from flask_restful import Resource, reqparse
from app import web3 as network
from app import sms as twilio
from app.usr.model import User
import app.twilio.responses as responses

class Client(Resource):

    sender = ""
    send_message = ""

    def post(self):
        """Recieve messages via Twilio."""
        User.delete_all()

        self.sender = request.form['From']
        self.sender_message = request.form['Body']
       
        if not User.exists(self.sender):
            # New user
            new_user = self.create_user(self.sender)
            self.send_message(responses.greeting)
            self.send_message(responses.commands)
        else:
            user = User.find_by_phonenumber(self.sender)

            """CHECK BALANCE"""


            """SEND ETHEREUM"""


        return {'status': 'OK'}, 200


    def create_user(self, sender):
        #user_account = network.eth.accounts.create(sender)
        #pprint.pprint(user_account)
        private_key = "test"#user_account['privateKey']

        new_user = User(
            phone = sender,
            private = private_key
        )

        new_user.save_to_db()
        return


    def send_message(self, message, reciever = None):
        if reciever is None:
            reciever = self.sender

        message = twilio.api.account.messages.create(
            to = reciever,
            from_ = "+18312641420",
            body = message
        )

        return


    def check_user_balance(self):
        pass


    def send_tokens(self):
        pass

        
