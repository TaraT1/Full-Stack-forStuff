#ref trivia. 
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

#TODO  Referencing bkshlf
database_name = "stuff"
database_path = "postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    # binds flask app and SQLAlchemy service
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
def db_drop_and_create_all():
    # Drops db tables. Can be used to initialie clean db
    db.drop_all()
    db.create_all()
'''

class Book(db.Model):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    subject = Column(String)
    genre = Column(String)
    description = Column(String)
    notes = Column(String)
    form = Column(String)
    location = db.relationship('Location', backref='Book', lazy=True)
    #future: Zotero integration
    #future: read - date last read

class Location(db.Model): #foreign_id in other models
    __tablename__ = 'Location'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    type = Column(String)
    description = Column(String)
    referenceid = Column(String)

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





