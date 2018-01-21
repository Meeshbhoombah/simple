# -*- encoding: utf-8 -*-
"""
tools.py

generate_random_string(string_length: int) = generate a string of random alphanumeric chars given
    a specefied length
"""

def generate_random_string(string_length):
    """ Generate a 16 character alphanumeric string

    Args:
    - self (Account): the Account object

    Returns:
    - random_char_string (String): a series of 16 random characters 
    """
    return "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(16))


