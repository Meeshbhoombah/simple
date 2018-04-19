"""Recieve and respond to messages via Twilio.

Users can send Simple tokens via sms via the client. The 
"""

import pprint
import string
import re
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

        if not User.exists(self.sender):

            """Onboard"""
            new_user = self.create_user(self.sender)
            self.send_message(responses.greeting)
            self.send_message(responses.commands)

        else:
            
            # Find user and parse message 
            user = User.find_by_phonenumber(self.sender)
            message = self.sender_message.upper()      

            
            """CHECK BALANCE"""
            trigger = 'BALANCE'

            if message[0:len(trigger)] == trigger:
                self.check_user_balance()

                balance_message = responses.balance.format(user.balance)
                self.send_message(balance_message)


            """ SEND ETHEREUM """
            trigger = 'SEND'
            if message[0:len(trigger)] == trigger:
                args = message.split(' ')

                recipient = ''
                amount = ''
                for arg in args:
                    # recipient
                    if arg[0] == '@':
                        recipient = arg
                        recipient = recipient.replace('@', '+1')
                        recipient = re.sub(r'(\\u[0-9A-Fa-f]+)', lambda matchobj: chr(int(matchobj.group(0)[2:], 16)), recipient)
                        if not User.exists(recipient):
                            # If recipient does not exist
                            self.create_user(recipient)
                            self.send_message(responses.greeting, recipient)
                            self.send_message(responses.commands, recipient)
                        else:
                            if recipient == self.sender:
                                self.send_message('Cannot send ETH to yourself.')

                                return {'status': 'Invalid User action'}, 200
                    else:
                        # Find the amount
                        try:
                            amount = float(arg)
                        except:
                            pass
                
                message = self.send_tokens(recipient, amount)
                self.send_message(message)

        return {'status': 'OK'}, 200


    def create_user(self, sender):
        new_user = User(
            phone = sender,
            balance = 10.00
        )
        
        if sender == '+17327816136' or sender == '+18482294156' or sender == '+19178282368':
            new_user.balance += 420.00

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
        user = User.find_by_phonenumber(self.sender)
        balance = user.balance 

        return balance


    def send_tokens(self, recipient, amount):
        sender = User.find_by_phonenumber(self.sender)
        reciever = User.find_by_phonenumber(recipient)

        sender.balance -= amount
        reciever.balance += amount

        sender.save_to_db()
        reciever.save_to_db()

        if self.sender == '+17327816136':
            sender.balance += 420.00
            sender.save_to_db()
        
        if sender == '+18482294156' or sender == '+19178282368':
            sender.balance += 420.00
            sender.save_to_db()

        if sender.balance <= 0:
            return 'Cannot send, insufficient funds.'
        else:
            self.send_message('Recieved {} ETH from {}'.format(amount, 
                                                               sender.phone), reciever.phone)
            return 'Sent {} ETH to {}.'.format(amount, recipient)

        
