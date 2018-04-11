# -*- encoding: utf-8 -*-

"""
tests/simple/__init__.py

Baseline testing class with a testing blockchain and other utilities for testing the 
Simple smart contract suite. 
"""

import unittest
from vyper import compiler
from ethereum.tools import tester
from ethereum.slogging import get_logger

class SimpleBlockchainBaseTestCase(unittest.TestCase):
    """Creates and configures the PyEthereum tester object for Simple. 
  
    Initalizes the PyEthereum tester object and binds it to the `SimpleTestingBlockchain`
    class which serves as the baseline configuration for testing the various Simple
    smart contracts. Variable names are in shorthand for writability.

    Attributes:
        t (tester): the PyEthereum tester object 
        s (tester.Chain()): the current stored state of the testing blockchain, 
            initalized with a genesis block
    """
    t = None
    s = None


    @classmethod
    def _listen_for_events(cls):
        """Listen and collect all testing blockchain events."""
        cls.events = []
        cls.s.head_state.log_listeners.append(
            lambda x: cls.events.append(cls.c.translator.listen(x))
        )


    @classmethod
    def setUpClass(cls, path_to_contract = None):
        """Bind the initalized testing blockchain to the SimpleTestingBlockchain class.
       
        Allows for one testing blockchain to be used for all test cases - utilizes the
        PyEthereum `revert()` method to return to a previously saved state called a 
        `snapshot`. 

        Args:
            cls (cls): the `SimpleTestingBlockchain` class
            path_to_contract (str): the path to the
        """
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

        cls.strict_log_mode = True
        cls._listen_for_events()

    
    def setUp(self, path_to_contract = None):
        """Revert to inital testing state and denote gas usage per test."""
        self.longMessage = True

        # reset the testing blockchain to the inital state
        self.s.revert(self.initial_state)

        self.inital_gas_used = self.b.head_state.gas_used
        self.inital_refund   = self.b.head_state.refunds

        get_logger('eth.pb.tx')
        get_logger('eth.pb.msg')

        if path_to_contract:
            self.deploy_contract(path_to_contract)
            self.initial_state = self.c.snapshot()


    def tearDown(self):
        """Print gas used per test."""
        gas_used = self.s.head_state.gas_used
        print("Test used {} gas".format(gas_used - self.inital_gas_used))


    def assertTxFailed(self, callable, exception = tester.TransactionFailed):
        """Assert a transaction has failed and revert to the inital state."""
        initial_state = self.s.snapshot()

        self.assertRaises(exception, callable)
        self.s.revert(initial_state)


    def deploy_contract(self, path_to_contract):
        """Deploy a compiled Vyper smart contract on the testing blockchain."""
        with open(path_to_contract, 'r') as in_file:
            contract_code = read()

            # compile contract and initalize on testing blockchain
            self.c = self.s.contract(contract_code, languages = 'vyper')


