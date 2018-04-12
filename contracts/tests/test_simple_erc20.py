# -*- encoding: utf-8 -*-

"""
test_simple_erc20.py

Test the smart contract implementing the ERC-20 compliant version of simple.
"""

import unittest
import ethereum.utils as utils
import ethereum.abi as abi
from contracts.tests.test_base import SimpleBaseTestCase


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
        self.deploy_contract(PATH_TO_CONTRACT)
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


    def test_totalSupply(self):
        # Test total supply initially, after deposit, between two withdraws, and after failed withdraw
        self.assertEqual(self.c.totalSupply(), 0)
        self.assertIsNone(self.c.deposit(value=2, sender=self.t.k1))
        self.assertEqual(self.c.totalSupply(), 2)
        self.assertTrue(self.c.withdraw(1, sender=self.t.k1))
        self.assertEqual(self.c.totalSupply(), 1)
        # Ensure total supply is equal to balance
        self.assertEqual(self.c.totalSupply(), self.s.head_state.get_balance(self.c.address))
        self.assertTrue(self.c.withdraw(1, sender=self.t.k1))
        self.assertEqual(self.c.totalSupply(), 0)
        self.assertTxFailed(lambda: self.c.withdraw(1, sender=self.t.k1))
        self.assertEqual(self.c.totalSupply(), 0)
        # Test that 0-valued deposit can't affect supply
        self.assertIsNone(self.c.deposit(value=0, sender=self.t.k1))
        self.assertEqual(self.c.totalSupply(), 0)

    def test_transfer(self):
        # Test interaction between deposit/withdraw and transfer
        self.assertTxFailed(lambda: self.c.withdraw(1, sender=self.t.k2))
        self.assertIsNone(self.c.deposit(value=2, sender=self.t.k1))
        self.assertTrue(self.c.withdraw(1, sender=self.t.k1))
        self.assertTrue(self.c.transfer(self.t.a2, 1, sender=self.t.k1))
        self.assertTxFailed(lambda: self.c.withdraw(1, sender=self.t.k1))
        self.assertTrue(self.c.withdraw(1, sender=self.t.k2))
        self.assertTxFailed(lambda: self.c.withdraw(1, sender=self.t.k2))
        # Ensure transfer fails with insufficient balance
        self.assertTxFailed(lambda: self.c.transfer(self.t.a1, 1, sender=self.t.k2))
        # Ensure 0-transfer always succeeds
        self.assertTrue(self.c.transfer(self.t.a1, 0, sender=self.t.k2))

    def test_transferFromAndAllowance(self):
        # Test interaction between deposit/withdraw and transferFrom
        self.assertTxFailed(lambda: self.c.withdraw(1, sender=self.t.k2))
        self.assertIsNone(self.c.deposit(value=1, sender=self.t.k1))
        self.assertIsNone(self.c.deposit(value=1, sender=self.t.k2))
        self.assertTrue(self.c.withdraw(1, sender=self.t.k1))
        # This should fail; no allowance or balance (0 always succeeds)
        self.assertTxFailed(lambda: self.c.transferFrom(self.t.a1, self.t.a3, 1, sender=self.t.k2))
        self.assertTrue(self.c.transferFrom(self.t.a1, self.t.a3, 0, sender=self.t.k2))
        # Correct call to approval should update allowance (but not for reverse pair)
        self.assertTrue(self.c.approve(self.t.a2, 1, sender=self.t.k1))
        self.assertEqual(self.c.allowance(self.t.a1, self.t.a2, sender=self.t.k3), 1)
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 0)
        # transferFrom should succeed when allowed, fail with wrong sender
        self.assertTxFailed(lambda: self.c.transferFrom(self.t.a2, self.t.a3, 1, sender=self.t.k3))
        self.assertEqual(self.c.balanceOf(self.t.a2), 1)
        self.assertTrue(self.c.approve(self.t.a1, 1, sender=self.t.k2))
        self.assertTrue(self.c.transferFrom(self.t.a2, self.t.a3, 1, sender=self.t.k1))
        # Allowance should be correctly updated after transferFrom
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 0)
        # transferFrom with no funds should fail despite approval
        self.assertTrue(self.c.approve(self.t.a1, 1, sender=self.t.k2))
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 1)
        self.assertTxFailed(lambda: self.c.transferFrom(self.t.a2, self.t.a3, 1, sender=self.t.k1))
        # 0-approve should not change balance or allow transferFrom to change balance
        self.assertIsNone(self.c.deposit(value=1, sender=self.t.k2))
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 1)
        self.assertTrue(self.c.approve(self.t.a1, 0, sender=self.t.k2))
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 0)
        self.assertTrue(self.c.approve(self.t.a1, 0, sender=self.t.k2))
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 0)
        self.assertTxFailed(lambda: self.c.transferFrom(self.t.a2, self.t.a3, 1, sender=self.t.k1))
        # Test that if non-zero approval exists, 0-approval is NOT required to proceed
        # a non-conformant implementation is described in countermeasures at
        # https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/edit#heading=h.m9fhqynw2xvt
        # the final spec insists on NOT using this behavior
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 0)
        self.assertTrue(self.c.approve(self.t.a1, 1, sender=self.t.k2))
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 1)
        self.assertTrue(self.c.approve(self.t.a1, 2, sender=self.t.k2))
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 2)
        # Check that approving 0 then amount also works
        self.assertTrue(self.c.approve(self.t.a1, 0, sender=self.t.k2))
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 0)
        self.assertTrue(self.c.approve(self.t.a1, 5, sender=self.t.k2))
        self.assertEqual(self.c.allowance(self.t.a2, self.t.a1, sender=self.t.k2), 5)


    def test_payability(self):
        # Make sure functions are appopriately payable (or not)

        # Payable functions - ensure success
        self.assertIsNone(self.c.deposit(value=2, sender=self.t.k1))
        # Non payable functions - ensure all fail with value, succeed without
        self.assertTxFailed(lambda: self.c.withdraw(0, value=2, sender=self.t.k1))
        self.assertTrue(self.c.withdraw(0, value=0, sender=self.t.k1))
        self.assertTxFailed(lambda: self.c.totalSupply(value=2, sender=self.t.k1))
        self.assertEqual(self.c.totalSupply(value=0, sender=self.t.k1), 2)
        self.assertTxFailed(lambda: self.c.balanceOf(self.t.a1, value=2, sender=self.t.k1))
        self.assertEqual(self.c.balanceOf(self.t.a1, value=0, sender=self.t.k1), 2)
        self.assertTxFailed(lambda: self.c.transfer(self.t.a2, 0, value=2, sender=self.t.k1))
        self.assertTrue(self.c.transfer(self.t.a2, 0, value=0, sender=self.t.k1))
        self.assertTxFailed(lambda: self.c.approve(self.t.a2, 1, value=2, sender=self.t.k1))
        self.assertTrue(self.c.approve(self.t.a2, 1, value=0, sender=self.t.k1))
        self.assertTxFailed(lambda: self.c.allowance(self.t.a1, self.t.a2, value=2, sender=self.t.k1))
        self.assertEqual(self.c.allowance(self.t.a1, self.t.a2, value=0, sender=self.t.k1), 1)
        self.assertTxFailed(lambda: self.c.transferFrom(self.t.a1, self.t.a2, 0, value=2, sender=self.t.k1))
        self.assertTrue(self.c.transferFrom(self.t.a1, self.t.a2, 0, value=0, sender=self.t.k1))

    def test_raw_logs(self):
        self.s.head_state.receipts[-1].logs = []
        # Check that withdraw appropriately emits Withdraw event
        self.assertTrue(self.c.withdraw(1, sender=self.t.k1))
        self.check_logs([self.transfer_topic, bytes_to_int(self.t.a1), 0], (1).to_bytes(32, byteorder='big'))
        self.assertTrue(self.c.withdraw(0, sender=self.t.k1))
        self.check_logs([self.transfer_topic, bytes_to_int(self.t.a1), 0], (0).to_bytes(32, byteorder='big'))

        # Check that transfer appropriately emits Transfer event
        self.assertTrue(self.c.transfer(self.t.a2, 1, sender=self.t.k1))
        self.check_logs([self.transfer_topic, bytes_to_int(self.t.a1), bytes_to_int(self.t.a2)], (1).to_bytes(32, byteorder='big'))
        self.assertTrue(self.c.transfer(self.t.a2, 0, sender=self.t.k1))
        self.check_logs([self.transfer_topic, bytes_to_int(self.t.a1), bytes_to_int(self.t.a2)], (0).to_bytes(32, byteorder='big'))

        # Check that approving amount emits events
        self.assertTrue(self.c.approve(self.t.a1, 1, sender=self.t.k2))
        self.check_logs([self.approval_topic, bytes_to_int(self.t.a2), bytes_to_int(self.t.a1)], (1).to_bytes(32, byteorder='big'))
        self.assertTrue(self.c.approve(self.t.a2, 0, sender=self.t.k3))
        self.check_logs([self.approval_topic, bytes_to_int(self.t.a3), bytes_to_int(self.t.a2)], (0).to_bytes(32, byteorder='big'))

        # Check that transferFrom appropriately emits Transfer event
        self.assertTrue(self.c.transferFrom(self.t.a2, self.t.a3, 1, sender=self.t.k1))
        self.check_logs([self.transfer_topic, bytes_to_int(self.t.a2), bytes_to_int(self.t.a3)], (1).to_bytes(32, byteorder='big'))
        self.assertTrue(self.c.transferFrom(self.t.a2, self.t.a3, 0, sender=self.t.k1))
        self.check_logs([self.transfer_topic, bytes_to_int(self.t.a2), bytes_to_int(self.t.a3)], (0).to_bytes(32, byteorder='big'))

        # Check that no other ERC-compliant calls emit any events
        self.s.head_state.receipts[-1].logs = []
        self.assertEqual(self.c.totalSupply(), 1)
        self.assertEqual(self.s.head_state.receipts[-1].logs, [])
        self.assertEqual(self.c.balanceOf(self.t.a1), 0)
        self.assertEqual(self.s.head_state.receipts[-1].logs, [])
        self.assertEqual(self.c.allowance(self.t.a1, self.t.a2), 0)
        self.assertEqual(self.s.head_state.receipts[-1].logs, [])

        # Check that failed (Deposit, Withdraw, Transfer) calls emit no events
        self.assertTxFailed(lambda: self.c.deposit(value=MAX_UINT256, sender=self.t.k1))
        self.assertEqual(self.s.head_state.receipts[-1].logs, [])
        self.assertTxFailed(lambda: self.c.withdraw(1, sender=self.t.k1))
        self.assertEqual(self.s.head_state.receipts[-1].logs, [])
        self.assertTxFailed(lambda: self.c.transfer(self.t.a2, 1, sender=self.t.k1))
        self.assertEqual(self.s.head_state.receipts[-1].logs, [])
        self.assertTxFailed(lambda: self.c.transferFrom(self.t.a2, self.t.a3, 1, sender=self.t.k1))
        self.assertEqual(self.s.head_state.receipts[-1].logs, [])


if __name__ == '__main__':
    unittest.main()

