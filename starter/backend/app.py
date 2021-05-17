import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)


'''
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
'''

#CORS headers
@app.after_request(response)
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

#Controllers
@app.route('/books', methods='[POST]')
def create_book():
  body = request.get_json()

  new_title = body.get('title', None)
  new_author = body.get('author', None)
  new_location = body.get('location', None)

  try:
    book = Book(title=new_title, author=new_author, location=new_location)
    book.insert
    return json
      'success': True,
      'created': book.id,
      'total_books': len(Book.query.all())
    }]

    except:
      abort(422)
      


return app