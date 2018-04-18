#!/usr/bin/env bash

echo "Starting Flask server..."

export FLASK_ENV=prod

git clone https://github.com/ethereum/vyper.git
cd /vyper

make
cd ../
rm -rf vyper/

python run.py

