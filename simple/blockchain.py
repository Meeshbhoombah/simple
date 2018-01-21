# -*- encoding: utf-8 -*-
"""
blockchain.py


- Defines a block
    + Uses module hashlib to hash blocks
"""

import hashlib as hash
from os.path import exists

class Block:

    def __init__(self, index, timestamp, data, prev_hash):
        """ Create a block given an index, timestamp, data, and the has of the previous 
            block.

            Args:
            - self (Block): the block object
            - index (int): the index at which the block exists within the blockchain
            - timestamp (Date): the DateTime at which a block was created
            - prev_hash (hash.sha256): the hash of the block prior to a given block
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash

    def hash(self):
        """ Compute the hash of a given block

            Args:
            - self (Block): the block object

            Returns:
            - the computed hash of a given block
        """
        sha = hash.sha256()
        sha.update(str(self.index) +
                   str(self.timestamp) +
                   str(self.data) +
                   str(prev_hash))

class Blockchain:

    def __init__(self, difficulty, local_store_path):
        """ Create an instance of a verified blockchain
            
            Args:
            - self (Blockchain): the blockchain object
        """
        self.difficulty = difficulty
        self.local_store_path = local_store_path

    def read_from_disk(self, file_path):
        """ Read in the local storage of a block
            
            Args:
            - self (Blockchain): the blockchain object
            - file_path (string): .csv file contain the blockchain
        """
        with open(file_path, "wr") as f:
            return f.read()

    def create_

