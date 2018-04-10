# -*- encoding: utf-8 -*-

"""
./simple/tests/simple/__init__.py

Baseline testing class with a testing blockchain.
"""

import unittest
from vyper import compiler
from ethereum.tools import tester
from ethereum.slogging import get_logger

class SimpleTestingBlockchain(unittest.TestCase):
    """Creates and configures the PyEthereum tester object for Simple. 
  
    Initalizes the PyEthereum tester object and binds it to the `SimpleTestingBlockchain`
    class which serves as the baseline configuration for testing the various Simple
    smart contracts. Variable names are in shorthand for writability.

    Attributes:
        t (tester): the PyEthereum tester object 
        s (tester.Chain()): the current stored state of the testing blockchain, 
            initalized with a genesis block
        c (ABIContract): The main contract compiled on the initalized PyEthereum test 
            network
    """
    t = None
    s = None
    c = None

    @classmethod
    def setUpClass(cls):
        """Initalizes the testing blockchain and funds accounts."""
        super(SimpleTestingBlockchain, cls).setUpClass()

        # bind the testing object to the class
        cls.t = tester

        # create a new test blockchain with a genesis block
        cls.s = cls.t.Chain()

        # fund accounts
        cls.s.head_state.gas_limit = 10**80
        cls.s.head_state.set_balance(cls.t.a0, 10**80)
        cls.s.head_state.set_balance(cls.t.a1, MAX_UINT256 * 3)
        cls.s.head_state.set_balance(cls.t.a2, utils.denoms.ether * 1)

        cls.initial_state = None

        # run vyper when requested
        cls.t.languages['vyper'] = compiler.Compiler()

    
    def setUp(self):
        """Configure and create defaults per test case."""
        self.longMessage = True

        # reset the testing blockchain to the inital state
        self.s.revert(self.initial_state)

        self.inital_gas_used = self.b.head_state.gas_used
        self.inital_refund   = self.b.head_state.refunds

        get_logger('eth.pb.tx')
        get_logger('eth.pb.msg')


    def tearDown(self):
        """Print gas used per test."""
        gas_used = self.s.head_state.gas_used
        print("Test used {} gas".format(gas_used - self.inital_gas_used))


    def assertTxFailed(self, callable, exception = tester.TransactionFailed):
        """Assert a transaction has failed and revert to the inital state."""
        initial_state = self.s.snapshot()

        self.assertRaises(exception, callable)
        self.s.revert(initial_state)


