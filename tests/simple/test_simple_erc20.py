# -*- encoding: utf-8 -*-

"""
test_simple_erc20.py

Test the smart contract implementing the ERC-20 compliant version of simple.
"""

import unittest
from . import SimpleBlockchainBaseTestCase

# Path to Simple ERC-20 Token smart contract
PATH_TO_CONTRACT = "simple/simple_ERC20.v.py"

class SimpleERC20TestCase(SimpleBlockchainBaseTestCase):
    """Tests the Simple ERC-20 Token Smart Contract."""
    
    def setUp(self):
        """"""
        super().setUp(PATH_TO_CONTRACT)

