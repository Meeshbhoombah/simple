#!/usr/bin/env bash

git clone https://github.com/ethereum/vyper.git
cd /vyper
make

cd ../
rm -rf vyper/

