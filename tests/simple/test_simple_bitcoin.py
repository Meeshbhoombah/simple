# -*- encoding: utf-8 -*-

'''
test_simple.py

Test the smart contract implementing the core Simple logic.
'''

import pytest

from vyper import compiler
from ethereum import tester

@pytest.fixture
def tester():
    ''' Compiles `simple.v.py` and binds it to the tester object

    Returns:
        tester (object): the configured testing client with the compiled      
            ABIContract (`tester.contract`) from which methods can be executed 
            on the tester chain
    '''
    # create a new test-blockchain with a genesis block
    chain = tester.Chain()
    
    # run vyper compiler when requested
    tester.languages["vyper"] = compiler.Compiler()

    contract_code = open("simple/simple.v.py").read()

    # compile and initalize the contract
    tester.contract = chain.contract(
        contract_code,
        languages = "vyper",
        args = []
    )

    return tester


def bytes32(plaintext):
    ''' Pads a string \x00 bytes to return the correct bytes32 representation

    Args:
         plaintext (str): the unpadded string to be converted to unicode and
            padded with `\x00` to match its bytes32 representation

    Returns:
         bytestext (bytes): the converted and padded bytes string of the 
            original plaintext
    '''
    bytestext = plaintext.encode()
    return bytestext + (32 - len(bytestext)) * b'\x00'


def test_initial_state(tester):
    assert tester.contract.name() == bytes32('simple')
    assert tester.contract.symbol() == bytes32('SMLP')
    assert tester.contract.totalSupply() == 0

    # test if Genesis block was created
    assert tester.contraact.chainLength() == 1

