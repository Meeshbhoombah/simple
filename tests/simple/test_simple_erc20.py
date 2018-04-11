# -*- encoding: utf-8 -*-

"""
test_simple_erc20.py

Test the smart contract implementing the ERC-20 compliant version of simple.
"""

import unittest
from tests.simple import SimpleBlockchainBaseTestCase

# Path to Simple ERC-20 Token smart contract
PATH_TO_CONTRACT = "simple/blockchain/simple_ERC20.v.py"

class SimpleERC20TestCase(SimpleBlockchainBaseTestCase):
    """Tests the Simple ERC-20 Token Smart Contract."""
   
    @classmethod
    def setUpClass(cls):
        """Reinitalize the setUp method with the ERC20 token smart contract."""
        super(SimpleERC20TestCase, cls).setUpClass(PATH_TO_CONTRACT)


    

