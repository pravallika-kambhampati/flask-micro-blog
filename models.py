from app import db
from sqlalchemy import DateTime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = password
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Blog(db.Model):
    __tablename__ = 'blogs'
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    text = db.Column(db.String(512))
    created_date = db.Column(db.String(128))

    def __init__(self,username,text,created_date):
        self.username=username
        self.text = text
        self.created_date = created_date 
    def __repr__(self):
        return '<id {}>'.format(self.id)    
