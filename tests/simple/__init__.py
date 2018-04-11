# -*- encoding: utf-8 -*-

"""
tests/simple/__init__.py

Baseline testing class with a testing blockchain and other utilities for testing the 
Simple smart contract suite. 
"""

import unittest
from vyper import compiler
from ethereum import utils
from ethereum.tools import tester
from ethereum.slogging import get_logger


MAX_UINT256 = (2 ** 256) - 1 # Maximum allowed uint256 value
MAX_UINT128 = (2 ** 128) - 1 # Maximum allowed num128 valie


class SimpleBaseTestCase(unittest.TestCase):
    """Creates and configures the PyEthereum tester object for Simple. 
  
    Initalizes the PyEthereum tester object and binds it to the `SimpleTestingBlockchain`
    class which serves as the baseline configuration for testing the various Simple
    smart contracts. Variable names are in shorthand for writability.

    Attributes:
        t (tester): the PyEthereum tester object 
        s (tester.Chain()): the current stored state of the testing blockchain, 
            initalized with a genesis block
        c (ABIContract): the compiled smart contract
    """
    t = None
    s = None
    c = None


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
        # maintain `unittest.Testcase` setUpClass logic
        super(SimpleBaseTestCase, cls).setUpClass()

        # bind the testing object to the class
        cls.t = tester

        # create a new test blockchain with a genesis block
        cls.s = cls.t.Chain()

        # fund accounts
        cls.s.head_state.gas_limit = 10**80
        cls.s.head_state.set_balance(cls.t.a0, 10**80)
        cls.s.head_state.set_balance(cls.t.a1, MAX_UINT256 * 3)
        cls.s.head_state.set_balance(cls.t.a2, utils.denoms.ether * 1)

        # run vyper when requested
        cls.t.languages['vyper'] = compiler.Compiler()

        cls.initial_state = None
        cls.strict_log_mode = True
        cls._listen_for_events()

    
    def setUp(self):
        """Revert to inital testing state and output gas usage per test."""
        self.longMessage = True

        # reset the testing blockchain to the inital state
        self.s.revert(self.initial_state)

        self.inital_gas_used = self.s.head_state.gas_used
        self.inital_refund   = self.s.head_state.refunds

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


    def deploy_contract(self, path_to_contract):
        """Deploy a compiled Vyper smart contract on the testing blockchain."""
        with open(path_to_contract, 'r') as in_file:
            contract_code = in_file.read()

            # compile contract and initalize on testing blockchain
            self.c = self.s.contract(contract_code, language = 'vyper')
           
            # if no contract is loaded save inital state of smart contract
            if self.initial_state is None:
                self.initial_state = self.s.snapshot()


    def check_logs(self, topics, data):
        """Searches through a topic to assert that a log was correctly made."""
        found = False
        for log_entry in self.s.head_state.receipts[-1].logs:
            if topics == log_entry.topics and data == log_entry.data:
                found = True

        self.assertTrue(found, self.s.head_state.receipts[-1].logs)


    @staticmethod
    def to_int(bytez):
        """Convert bytes to int."""
        return int(utils.encode_hex(bytez), 16)

    
    @staticmethod
    def to_bytes(i):
        """Convert int to bytes."""
        return int(i).to_bytes(32, byteorder = 'big')


if __name__ == '__main__':
    unittest.main()

