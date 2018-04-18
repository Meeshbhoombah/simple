#!usr/bin/python3
"""Model for `users` table.

The user data for Simple is stored off-chain for minimal gas usage, etc
"""

from flask_sqlalchemy import SQLAlchemy

user_db = SQLAlchemy()

class User(user_db.Model):
    __tablename__ = 'users'

    id = user_db.Column(user_db.Integer, primary_key = True)
    username = user_db.Column(user_db.String(120), unique = True, nullable = True)
    phone = user_db.Column(user_db.String(12), unique = True, nullable = False)
    private = user_db.Column(user_db.String(120), unique = True, nullable = True)
    balance = user_db.Column(user_db.String(120), unique = False, nullable = True)
    first_name = user_db.Column(user_db.String(20), unique = False, nullable = True)
    created_on = user_db.Column(user_db.DateTime, default=user_db.func.now())
    updated_on = user_db.Column(user_db.DateTime, default=user_db.func.now(), onupdate=user_db.func.now())

    def save_to_db(self):
        user_db.session.add(self)
        user_db.session.commit()
    
    @classmethod
    def exists(cls, phone):
        exists = cls.query.filter_by(phone = phone).scalar() is not None

    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()


    @classmethod
    def find_by_phonenumber(cls, phone):
        return cls.query.filter_by(phone = phone).first()

    
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = user_db.session.query(cls).delete()
            user_db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

