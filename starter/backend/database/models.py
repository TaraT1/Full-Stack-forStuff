#ref trivia. 
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# db name, path (trivia)
database_name = "stuff"
database_path = "postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', database_name)

db = SQLAlchemy()

'''
def setupdb(app)
    # binds flask app to SQLAlchemy service
'''