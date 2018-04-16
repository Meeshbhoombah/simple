#!usr/bin/python3
"""Main entrypoint into 'Simple SMS Client' Flask and SQL application.

Demonstates functionality of the simple blockchain and smart contracts in a 
tangible way.

License: MIT
Website:
"""


from config import config
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)

# Using config object from `config.py`
app.config.from_object(config['default']) 
config['default'].init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{usr}:{dbpass}@{host}:5432/{db}'.format(
    usr = app.config['DBUSER'],
    dbpass = app.config['DBPASS'],
    host = app.config['DBHOST'],
    db = app.config['DBNAME']
)

@app.before_first_request
# TODO: init database

if __name__ == '__main__':
    app.run(host='0.0.0.0')


