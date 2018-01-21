# -*- encoding: utf-8 -*-
"""
account.py

"""

import random
import tools

class Account:

    def __init__(self, seed_money = 0):
        self.bal = seed_money
        self.address = generate_random_string(16)

    def generate_random_name(string):
        """ Generate a 16 character alphanumeric string

            Args:
            - self (Account): the Account object
        
            Returns:
            - random_char_string (String): a series of 16 random characters 
        """
        random_char_string = "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(16))

        return random_char_string
        

