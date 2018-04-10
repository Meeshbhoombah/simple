# -*- encoding: utf-8 -*-

'''
./simple/tests/simple/__init__.py

Baseline testing class with a testing blockchain.
'''

import os
import unittest
from ethereum import tester



class SimpleTestingBlockchain(unittest.TestCase):
    ''' Creates and configures the PyEthereum tester object for Simple. 
  
    Initalizes the PyEthereum tester object and binds it to the `SimpleTestingBlockchain`
    class which serves as the baseline configuration for testing the various Simple
    smart contracts.

    Attributes:
        t (tester): the PyEthereum tester object 
        b (tester.Chain()): a testing blockchain with a genesis block 
        c (ABIContract): The main contract compiled on the initalized PyEthereum 
            test network
    '''

    t = None
    b = None
    c = None

    @classmethod
    def setUpClass(cls):
        super(SimpleTestingBlockchain, cls).setUpClass()

        # bind the testing object to the class
        cls.t = tester

        # create a new test blockchain with a genesis block
        cls.b = cls.t.Chain()

        # configure accounts
        cls.b.head_state.gas_limit = 10**80
        cls.b.head_state.set_balance(cls.t.a0, 10**80)
        cls.b.head_state.set_balance(cls.t.a1, MAX_UINT256 * 3)
        cls.b.head_state.set_balance(cls.t.a2, utils.denoms.ether * 1)
        cls.initial_state = None

    
    def setUp(self):
        ''' Configure and create defaults per test case '''
        self.longMessage = True

        # reset the testing blockchain to the inital state
        self.b.revert(self.initial_state)

        self.inital_gas_used = self.b.head_state.gas_used
        self.inital_refund   = self.b.head_state.refunds

        



