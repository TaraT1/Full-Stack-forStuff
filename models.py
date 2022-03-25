import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
import json
from dotenv import load_dotenv

#For local development
ENV = 'dev'

if ENV == 'dev':
    database_path = 'postgresql://postgres:postgres@localhost:5432/stuff'

'''
#For production
load_dotenv()

database_path = os.getenv('DATABASE_URL')
'''
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
'''
def db_drop_and_create_all():
    # Drops db tables. Can be used to initialize clean db
    db.drop_all()
    db.create_all()
'''

#Models
class Location(db.Model): 
    __tablename__ = 'Location'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    #description = db.Column(db.String())
    #referenceid = db.Column(db.String())
    books = db.relationship('Book', backref='Location') 

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'type': self.type
        }

class Book(db.Model):
    __tablename__ = 'Book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    #subject = db.Column(db.String())
    #genre = db.Column(db.String())
    #description = db.Column(db.String())
    #notes = db.Column(db.String())
    form = db.Column(db.String())
    # ForeignKey to link books and locations
    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'))
    #future: Zotero integration
    #future: read - date last read


    def __init__(self, title, author, form, location_id):
        self.title = title
        self.author = author
        self.form = form
        self.location_id = location_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'title': self.title,
          'author': self.author,
          'form': self.form,
          'location_id': self.location_id
        }