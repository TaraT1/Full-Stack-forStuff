import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import Unauthorized
#?create_app; Trivia has def create_app
from models import setup_db, Location, Book
from dotenv import load_dotenv

load_dotenv() #loads environment variables

#assigning env variables
USER = os.environ.get('user_jwt')
OWNER = os.environ.get('owner_jwt')

def get_headers(token):
    return {'Authorization': f'Bearer {token'}}

#???app = Flask(__name__)
#API Testing 4.2

class StuffTestCase(unittest.TestCase):
    def setUp(self):#from trivia
        """Executed before each test. Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_db"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        #bind app to current context - ?? What is context?
        with self.app.app_context():
            self.db = SQLAlchemy
            self.db.init_app(self.app)
            #create tables
            self.db.create_all()

        #create new location record for testing
        self.new_location = {
            "name": "shelf ds1",
            "type": "bookshelf"
        }

        #create new book for testing
        self.new_book_0 = {
            "title": "", 
            "author": "", 
            "form": ""
        }

        self.new_book_1 = {
            "title": "Title1", 
            "author": "Author1", 
            "form": "ebook"
        }

         self.new_book_2 = {
            "title": "Title2", 
            "author": "Author2", 
            "form": "form2",
            "location_id": 2
        } 
        
        self.new_book_3 = {
            "title": "Title3", 
            "author": "Author3", 
            "form": "book",
            "location_id": 1
        }

    def tearDown(self):
        """Executed after reach test"""
        pass



    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    #LOCATION TESTS cf https://knowledge.udacity.com/questions/200723
    def test_post_location_auth(self):#payload required
        res = self.client().post('/locations/add', 
            json=self.new_location, 
            headers=get_headers(OWNER))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_locations'])
    
    def test_post_location_not_auth(self):#payload required
        res = self.client().post('/locations/add', 
            json=self.new_location) 

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['success'], False)
        self.assertTrue(data['message'], 'Unauthorized')


    def test_get_location(self):
        res = self.client().get('/locations')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['locations'])
        self.assertTrue(data['number of locations'])

    def test_get_locations_when_none(self):# Should self be none?
        res = self.client().get('locations')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['locations'])
        self.assertTrue(data['number of locations'])
    
    def test_update_location_authorized(self): #payload
        res = self.client().patch('locations/1', 
        json={'name': 'upshelf'},
        headers=get_headers(OWNER))

        data = json.loads(res.data)
        location = Location.query.filter(Location.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['location.id'])

    def test_update_location_not_auth(self):
        res = self.client().patch('location/1'),
        json={'name': 'upshelf'})

        data = json.loads(res.data)
        location = Location.query.filter(Location.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], Unauthorized)


    def test_delete_location_authorized(self):
        res = self.client().delete('locations/1',
        headers=get_headers(OWNER))

        data = json.loads(res.data)
        
        location = Location.query.filter(Location.id == 1).one_or_none()

        self.assertEqual(res.statust_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(location, None)

    def test_delete_location_not_auth(self):
        res = self.client().delete('locations/1')

        data = json.loads(res.data)

        location = Location.query.filter(Location.id == 1).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(location, None)

    #BOOK TESTS
    def test_post_book_auth(self): # payload reqd, + location
        res = self.client().post('/books/add',
            json=self.new_book_1,
            headers=get_headers(OWNER))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(['success'], True)
        self.assertTrue(['created'])
        self.assertTrue(['total_books'])

    def test_post_book_not_auth(self): # payload required
        res = self.client().post('/books/add', 
            json=self.new_book_1)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['success'], False)
        self.assertTrue(data]['message'], 'Unauthorized')


    def test_get_books(self): #no auth ndd
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success', True])
        self.assertTrue(data(['total_books']))

    #test if no books found
    
    def update_book_authorized(self):
        res = self.client().patch('books/1',
        json={'title': 'Changed_Title'},
        headers=get_headers(OWNER))

        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['book.id'])

    def update_book_not_authorized(self):
        res = self.client().patch('books/1',
        json={'title': 'Changed_Title'})
    
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], Unauthorized)

    def delete_book_auth(self): #requires auth
        res = self.client().delete('books/1',
        json=self.new_book_1,
        headers=get_headers(OWNER))

        data = json.loads(res.data)

        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(book, None)

    def delete_book_not_authorized(self):
        res = self.client().delete('books/1',
        json=self.new_book_1)

        data = json.loads(res.data)

        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], Unauthorized

# Make the tests executable
if __name__ == "__main__":
unittest.main()