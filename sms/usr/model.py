#!usr/bin/python3
"""Model for `users` table.

The user data for Simple is stored off-chain for minimal gas usage, etc
"""

from app import db

class User(db.Model):

    __tablename__ == 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    phone = db.Column(db.Integer(10)), unique = True, nullable = False)
    address = db.Column(db.String(120), unique = True, nullable = False)
    balance = db.Column(db.String(120), unique = False, nullable = True)
    first_name = db.Column(db.String(20)), unique = False, nullable = True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()


    @classmethod
    def find_by_phonenumber(cls, phonenumber):
        return cls.query.filter_by(phonenumber = phonenumber).first()

    
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

