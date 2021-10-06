import os
import json
from flask import Flask, render_template, request, Response, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from flask_migrate import Migrate
from models import Location, Book
from sqlalchemy.ext.declarative.api import declarative_base
from werkzeug.exceptions import Unauthorized
from jose import jwt
from auth import AuthError, requires_auth 

#from models import setup_db - Integrating models.py in app.py

ITEMS_PER_PAGE = 10

def paginate(request, selection):
  page = request.arts.get('page', 1, type=int)
  start = (page - 1) * ITEMS_PER_PAGE
  end = start + ITEMS_PER_PAGE

  items = [items.format() for book in selection] #specify items. Books, Locations, etc inclusive
  current_items = items[start:end]
  
  return current_items


app = Flask(__name__)
#cors = CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/stuff'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#db.create_all() - using migrate to sync, so no db.create_all() 

#Access-Control-Allow
@app.after_request
def after_request(response):
  #response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
  return response
  
'''
#Models **Separate to models.py. Problem is flask migrate is not picking it up
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

#Controllers
#LOCATIONS
@app.route('/locations/add', methods=['POST'])
@requires_auth('post:locations')
def create_locations(payload):
  #json
  data=request.get_json()

  new_name=data.get('name')
  new_type=data.get('type')

  if data is None:
    abort(404)

  try:
    location = Location(
      name=new_name,
      type=new_type
    )

    location.insert()

    locations = Location.query.all()

    return jsonify({
      'success': True,
      'created': location.id,
      'total_locations': len(locations)
    }), 200

  except Exception as e:
    print("Add LocAdd Exception >> ", e)
    abort(422)

@app.route('/locations', methods=['GET'])
@requires_auth('get:locations')
def get_locations(payload):

  try:
    locations=Location.query.all()
    get_locations = [location.format() for location in locations]
    return jsonify({
      'success': True,
      'locations': get_locations,
      'number of locations': len(locations)
    }), 200

  except Exception as e:
    print('GetLoc Exception >> ', e)
    abort(404)

##Update specific location
@app.route('/locations/<int:location_id>', methods=['PATCH'])
@requires_auth('patch:location')
def update_location(payload, location_id):

  data = request.get_json()

  if data is None:
    abort(404)

  try:
    location = Location.query.filter(Location.id==location_id).one_or_none()

    if location is None:
      abort(404)

    # update fields
    location.name = data.get('name', None)
    location.type = data.get('type', None)

    location.update()

    return jsonify({
      'success': True,
      'location.id': location_id
    }), 200

  except Exception as e:
    print ("Patch Location Exception >> ", e)
    abort(404)

#Delete location
@app.route('/locations/<int:location_id>', methods=['DELETE'])
@requires_auth('delete:location')
def delete_location(payload, location_id):

  try:
    location = Location.query.filter(Location.id==location_id).one_or_none()

    if location is None:
      abort(404)

    location.delete()

    return jsonify({
      'success': True,
    }, 200)

  except Exception as e:
    print("Delete location Exception >> ", e)
    abort(404)

# BOOKS
@app.route('/books/add', methods=['POST'])
@requires_auth('post:book') 
def create_book(payload):
  ''' Form
  new_title=request.form.get('title', '')

  new_form=request.form.get('form', '')
  new_location=request.form.get('location_id', '')
  '''
  #json
  data=request.get_json()

  new_title=data.get('title')
  new_author=data.get('author')
  new_form=data.get('form')
  new_location=data.get('location_id')

  if data is None:
    abort(404)

  try:
    book = Book(
      title=new_title, 
      author=new_author, 
      form=new_form,
      location_id=new_location
      )
      
      
    
    book.insert()
    db.session.add(book)
    db.session.commit()
    #return redirect(url_for('index.html')) #not sure of format for redirect
    
    return jsonify({
      'success': True,
      'created': book.id,
      'total_books': len(Book.query.all())
    }), 200

  except Exception as e:
    print("Add Book Exception >> ", e)
    abort(422)

@app.route('/books', methods = ['GET'])
@requires_auth('get:books')
def get_books(payload):

  try:
    books = Book.query.all()
    get_books = [book.format() for book in books]

    if books is None:
      abort(404) #resource not found

    return jsonify({
      'books': get_books,
      'success': True,
      'total_books': len(get_books)
    }, 200)

  except Exception as e:
    print("Get Exception >> ", e)
    abort(422)

@app.route('/books/<int:book_id>', methods=['PATCH'])
@requires_auth('patch:book')
def update_book(payload, book_id):
  
  data = request.get_json()

  if data is None:
    abort(404)

  try:
    book = Book.query.filter(Book.id==book_id).one_or_none()
    
    if book is None:
      abort(404)
    
    #*** Updates all fields*** 
    book.title = data.get('title', None)
    book.author = data.get('author', None)
    book.form = data.get('form', None)
    book.location = data.get('location_id', None)
    
    book.update()

    return jsonify({
      'success': True,
      'book.id': book_id
      #'book.location': location_id
    }, 200)

  except Exception as e:
    print ("Patch Book Exception >> ", e)
    abort(404)

@app.route('/books/<int:book_id>', methods=['DELETE'])
@requires_auth('delete:book')
def delete_book(payload, book_id):
  try:
    book = Book.query.filter(Book.id==book_id).one_or_none()

    if book is None:
      abort(404)

    book.delete()

    return jsonify({
      'success': True,
    }), 200

  except Exception as e:
    print("Delete Book Exception >> ", e)
    abort(404)

# Error Handlers for expected errors 
@app.errorhandler(404)
def not_found(error):
    return jsonify({
    "success": False,
    "error": 404,
    "message": "resource not found"
  }), 404

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
    "success": False,
    "error": 422,
    "message": "unprocessable"
  }), 422

# Error handlers for auth errors
@app.errorhandler(403)
def forbidden(error):
  return jsonify({
    "success": False,
    "error": "Access is forbidden"
    }), 403

@app.errorhandler(401)
def unauthorized(error):
  return jsonify({
    "success": False,
    "error": 401,
    "message": Unauthorized
  }), 401

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
  app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
#return app
'''