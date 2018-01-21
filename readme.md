# Simple
A bare-bones cryptocurrency implemented in Python.

## Installation
1. Clone this repository.
```
$ git clone https://github.com/Meeshbhoombah/simple
```

2. Create and run a virtualenv (recommended BUT not required).
```
$ virtualenv venv
New python executable in /Users/usr/Desktop/venv/bin/python
Installing setuptools, pip, wheel...done.

$ . venv/bin/activate
```
After running `. venv/bin/activate` you should see the virtualenv active
in the shell.

3. Install requirements.txt.
```
$ pip install -r requirements.txt
```

4. Add the flask server and run it.
```
$ export FLASK_APP=run.py
$ flask run
```
The simple node should now be running on your local machine.

## Todo
[ ] Barebones Flask server
[ ]

## Features
- [ ] Transaction State-based machine
- [ ] Account System
    - External accounts
    - Contract account
- [ ] Secured and validated transactions/state transactions
- [ ] Dynamicly sending Smart Contracts addresses
    - GAS to deloy contract
    - GAS to run contract
- [ ] Cryptocurrency


- [ ] Runnable Terminal Node:
    + [ ] Clone Blockchain (DNS Server lookup)
    + [ ] Simple terminal commands

