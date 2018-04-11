# -*- encoding: utf-8 -*-

'''
bin/test.py

Script for running the Simple test suite.

TODO: Add silent option for running tests
'''


import click
import unittest
from tests import *


@click.command()
def main():
    print("Running Simple test suite...")
    success = True

    # find all tests
    suite = unittest.TestLoader().discover('tests', pattern='tests*.py')

    res = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromModule(suite)
    )

    success &= res.wasSuccessful()
    print("All tests passed successfully...")


if __name__ == '__main__':
    main()

