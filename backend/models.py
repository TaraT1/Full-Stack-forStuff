#ref trivia. Integrated models into app.py, changed dir structure
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
#from flask_migrate import Migrate
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/stuff'
db = SQLAlchemy()

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
    book = db.relationship('Book', backref='Location', lazy=True) #Book refers to class

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
    location_id = db.Column(db.Integer, db.ForeignKey('Location.id')) #fkey refers to actual table
    #future: Zotero integration
    #future: read - date last read

    def __init__(self, title, author, form):
        self.title = title
        self.author = author
        self.form = form

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

'''
class Book(db.Model):
    __tablename__ = 'Book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    #subject = db.Column(db.String)
    #genre = db.Column(db.String)
    #description = db.Column(db.String)
    #notes = db.Column(db.String)
    form = db.Column(db.String)
    location_id = db.relationship('Location', backref='Book', lazy=True)
    #future: Zotero integration
    #future: read - date last read

    def __repr__(self):
        return f'<Book ID: {self.id}, title: {self.title}, author: {self.author}, form: {self.form}>' 

class Location(db.Model): #foreign_id in other models
    __tablename__ = 'Location'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    #description = db.Column(db.String)
    #referenceid = db.Column(db.String)
    book_id = db.Column(db.Integer. db.ForeignKey('Book.id'))

    def __repr__(self):
        return f'<Location ID: {self.id}, name: {self.name}, type: {self.type}>'

#db.create_all() - using migrate to sync db
'''


'''
class Video(db.Model):
    __tablename__ = 'Video'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    subject = Column(String)
    genre = Column(String)
    description = Column(String)
    notes = Column(String)
    form = Column(String)
    location = Column(String)

class Audio(db.Model):
    __tablename__ = 'Audio'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    subject = Column(String)
    genre = Column(String)
    description = Column(String)
    notes = Column(String)
    form = Column(String)
    location = Column(String)

class Object(db.Model):
    __tablename__ = 'Object'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    description = Column(String)
    notes = Column(String)
    form = Column(String)
    location = Column(Integer)
'''





