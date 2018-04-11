# -*- encoding: utf-8 -*-

"""
test_simple_erc20.py

Test the smart contract implementing the ERC-20 compliant version of simple.
"""

import unittest
import ethereum.utils as utils
import ethereum.abi as abi
from tests.simple import SimpleBaseTestCase


#PATH_TO_CONTRACT = "simple/blockchain/simple_ERC20.v.py"
PATH_TO_CONTRACT = "simple/ERC20.v.py"

MAX_UINT256 = (2 ** 256) - 1 # Maximum allowed uint256 value
MAX_UINT128 = (2 ** 128) - 1 # Maximum allowed num128 valie


class SimpleERC20TestCase(SimpleBaseTestCase):
    """Tests the Simple ERC-20 Token Smart Contract."""
   
    @classmethod
    def setUpClass(cls):
        """Reinitalize the setUp method with the ERC20 token smart contract."""
        super(SimpleERC20TestCase, cls).setUpClass(PATH_TO_CONTRACT)


    def setUp(self):
        """Run test setUp and generate log signatures."""
        super(SimpleERC20TestCase, self).setUp()
        self.log_sigs = {
            'Transfer' : self.to_int(utils.sha3("Tranfer(address,address,uint256)")),
            'Approval' : self.to_int(utils.sha3("Approval(address,address,uint256"))
        }

   
   def test_initial_state(self):
        # Check total supply is 0
        self.assertEqual(self.c.totalSupply(), 0)
        # Check several account balances as 0
        self.assertEqual(self.c.balanceOf(self.t.a1), 0)
        self.assertEqual(self.c.balanceOf(self.t.a2), 0)
        self.assertEqual(self.c.balanceOf(self.t.a3), 0)
        # Check several allowances as 0
        self.assertEqual(self.c.allowance(self.t.a1, self.t.a1), 0)
        self.assertEqual(self.c.allowance(self.t.a1, self.t.a2), 0)
        self.assertEqual(self.c.allowance(self.t.a1, self.t.a3), 0)
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a3), 0)


if __name__ == '__main__':
    unittest.main()

