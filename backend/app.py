import os
import json
from flask import Flask, render_template, request, Response, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Location, Book
from sqlalchemy.ext.declarative.api import declarative_base
from werkzeug.exceptions import Unauthorized
from auth import AuthError, requires_auth 

ITEMS_PER_PAGE = 10

'''
def paginate(request, selection):
  page = request.arts.get('page', 1, type=int)
  start = (page - 1) * ITEMS_PER_PAGE
  end = start + ITEMS_PER_PAGE

  items = [items.format() for book in selection] #specify items. Books, Locations, etc inclusive
  current_items = items[start:end]
  
  return current_items
'''
''' from trivia
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
def create_app(test_config=None):#trivia and coffee
    #create and configure
    app = Flask(__name__)
    setup_db(app)
    
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    #db.create_all() - using migrate to sync, so no db.create_all() 

    #Access-Control-Allow
    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
      return response
      
    #Controllers
    #LOCATIONS
    @app.route('/locations/add', methods=['POST'])
    @requires_auth('post:location')
    def create_location(payload):
      try:
        #json
        data=request.get_json()

        new_name = data.get('name')
        new_type = data.get('type')

        if data is None:
          abort(404)

        location = Location(
          name=new_name,
          type=new_type
        )

        location.insert()
        
        return jsonify({
          'success': True,
          'created': location.id,
          'total_locations': len(Location.query.all())
        }), 200

      except Exception as e:
        print("Add LocAdd Exception >> ", e)
        abort(422)

    @app.route('/locations', methods=['GET'])
    def get_locations():

      try:
        locations=Location.query.all()
        get_locations = [location.format() for location in locations]

        if locations is None:
          abort(404) #resource not found

        return jsonify({
          'success': True,
          'locations': get_locations,
          'total_locations': len(locations)
        }), 200

      except Exception as e:
        print('GetLoc Exception >> ', e)
        abort(422)

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

        if 'name' in data:
          location.name = data['name']
        if 'type' in data:
          location.type = data['type']

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
    def get_books():

      try:
        books = Book.query.all()
        get_books = [book.format() for book in books]

        if books is None:
          abort(404) #resource not found

        return jsonify({
          'success': True,
          'books': get_books,
          'total_books': len(books)
        }), 200

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
        
        if 'title' in data:
          book.title = data['title']
        if 'author' in data:
          book.author = data['author']
        if 'form' in data:
          book.form = data['form']
        if 'location_id' in data:
          book.location_id = data['location_id']
          #if location_id is None: Location does not exist. Please correct or create new location

        book.update()

        return jsonify({
          'success': True,
          'book.id': book_id
        }), 200

        '''
        return jsonify({
          'success': True,
          'book.id': book_id,
          'book.location_id': location_id
        }), 200
        
        '''
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
    @app.errorhandler(AuthError)
    def auth_error(error):
      return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
      }), error.status_code

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
        "message": "Unauthorized"
      }), 401

    @app.errorhandler(500)
    def internal(error):
      return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
      }), 500
      
    return app
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