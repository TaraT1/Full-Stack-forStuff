import json
from flask import Flask, render_template, request, Response, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from flask_migrate import Migrate

#from models import setup_db - Integrating models.py in app.py

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
  
#Models
class Location(db.Model): 
    __tablename__ = 'Location'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    type = db.Column(db.String())
    #description = db.Column(db.String())
    #referenceid = db.Column(db.String())
    book = db.relationship('Book', backref='Location', lazy=True)

    def __repr__(self):
        return f'<LocationID: {self.id}, name: {self.name}, type: {self.type}>'


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
    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'))
    #future: Zotero integration
    #future: read - date last read

    def __repr__(self):
        return f'<BookID: {self.id}, title: {self.title}, author: {self.author}, form: {self.form}>' 


#Controllers
#Locations
@app.route('/locations/add', methods=['POST'])
def create_locations():
  data=request.get_json()

  new_name=data.get('name')
  new_type=data.get('type')

  try:
    location = Location(
      name=new_name,
      type=new_type
    )

    location.insert()

    return jsonify({
      'success': True,
      'created': location.id,
      'total_locations': len(Location.query.all())
    })

  except Exception as e:
    print("Add LocAdd Exception >> ", e)
    abort(422)

@app.route('/locations', methods=['GET'])
def get_locations():

  try:
    locations=Location.query.all()
    #get_locations = [location.format() for location in locations]
    for location in locations:
      location.id = Location.id
      location.name = Location.name
      location.type = Location.type

      '''
      location_detail = {
        "location_id": location.id,
        "location_name": location.name,
        "location_type": location.type
      }
      #get_locations = data.append(location_detail)
      '''

    return jsonify({
      'success': True,
      'number of locations': len(locations)
    })

  except Exception as e:
    print('GetLoc Exception >> ', e)
    abort(404)

##LOCATIONS - Patch, delete

@app.route('/books/add', methods=['POST'])
def create_book():
  ''' Form
  new_title=request.form.get('title', '')

  new_form=request.form.get('form', '')
  new_location=request.form.get('location', '')
  '''
  #json
  data=request.get_json()

  new_title=data.get('title')
  new_author=data.get('author')
  new_form=data.get('form')
  new_location=data.get('location')

  try:
    book = Book(
      title=new_title, 
      author=new_author, 
      form=new_form, 
      location=new_location
      )
    
    book.insert()
    #db.session.add(book)
    #db.session.commit()
    #return redirect(url_for('index.html')) #not sure of format for redirect
    
    return jsonify({
      'success': True,
      'created': book.id,
      'total_books': len(Book.query.all())
    })

  except Exception as e:
    print("Add Exception >> ", e)
    abort(422)

@app.route('/books', methods = ['GET'])
def get_books():

  try:
    get_books = Book.query.all()
    for book in get_books:
      book.id = Book.id 
      book.title = Book.title

    return jsonify({
      'success': True,
      'total_books': len(get_books)
    })

  except Exception as e:
    print("Get Exception >> ", e)
    abort(422)

@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
  try:
    book = Book.query.filter(Book.id==book_id).one_or_none()
    #TODO need form for updates

    if book is None:
      abort(404)

    book.update()

    return jsonify({
      'success': True,
    })

  except Exception as e:
    print ("Patch Exception >> ", e)
    abort(404)

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
  try:
    book = Book.query.filter(Book.id==book_id).one_or_none()

    if book is None:
      abort(404)

    book.delete()

    return jsonify({
      'success': True,
    })

  except Exception as e:
    print("Delete Exception >> ", e)
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