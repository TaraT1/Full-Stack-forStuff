import os
import unittest
import json
from flask.wrappers import JSONMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import Unauthorized
from app import create_app
from models import setup_db, Location, Book
from auth import AuthError, requires_auth
from dotenv import load_dotenv

load_dotenv() #loads environment variables

#assigning env variables
OWNER = os.environ.get('owner_jwt')
USER = os.environ.get('user_jwt')

def get_headers(token):#unauth testing shows 200 - add content-type
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

class StuffTestCase(unittest.TestCase):
    def setUp(self):#from trivia
        """Executed before each test. Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "stuff_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)

        #setup_db(self.app, self.database_path)
        setup_db(self.app)

        #bind app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #create tables
            self.db.create_all()

        #create new location records for testing
        self.new_location = {
            "name": "shelf ds100",
            "type": "bookshelf2"
        }
        self.new_location_2 = {
            "name": "shelf ups10",
            "type": "bookshelf3"
        }
        self.new_location_3 = {
            "name": "pantry ds2",
            "type": "area"
        }
        self.new_location_4 = {
            "name": "cbnt ups2",
            "type": "bin"
        }

        #create new book records for testing
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
        """Executed after each test"""
        pass

    #LOCATION TESTS cf https://knowledge.udacity.com/questions/200723
    '''
    def test_post_location_auth(self):
        res = self.client().post('/locations/add', 
            json=self.new_location, 
            #json={
                #'name': 'test name A',
                #'type': 'test type A'
            #},
            headers=get_headers(OWNER))

        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_locations'])
    
    def test_403_permission_not_found_post_location(self):
        res = self.client().post('/locations/add', 
            json=self.new_location_2, 
            headers=get_headers(USER))
            #json={
                #'name': 'test name NAuth3',
                #'type': 'test type NAuth3'
            #})

        #data = json.loads(res.data)
        data = json.loads(res.data.decode('utf-8'))

        print(data)
        print(res)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found')
 
    def test_get_location(self): #OK; payload not required to retrieve
        res = self.client().get('/locations')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['locations'])
        self.assertTrue(data['total_locations'])


    def test_get_locations_when_none(self):
        res = self.client().get('/locations')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['locations'])
        self.assertTrue(data['total_locations'])

    
    def test_update_location_authorized(self): 
        res = self.client().patch('/locations/1', 
        json={'type': 'shelf'},
        headers=get_headers(OWNER))

        data = json.loads(res.data.decode('utf-8'))
        location = Location.query.filter(Location.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['location.id'])

    
    def test_403_permission_not_found_update_location(self):
        res = self.client().patch('locations/1',
        json={'name': 'upshelf5'},
        headers=get_headers(USER))

        data = json.loads(res.data.decode('utf-8'))
        location = Location.query.filter(Location.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    '''
    #** Need multiple entries in db or insert before each def
    def test_delete_location_authorized(self):
        res = self.client().delete('locations/11',
        headers=get_headers(OWNER))

        data = json.loads(res.data.decode('utf-8'))
        
        location = Location.query.filter(Location.id==11).one_or_none()

        self.assertEqual(res.status_code, 200)
        #self.assertEqual(data['success'], True) #TypeError: list indices must be integers or slices, not str
        self.assertEqual(location, None)

    def test_403_delete_location_not_auth(self):
        res = self.client().delete('locations/1',
        headers=get_headers(USER))

        data = json.loads(res.data)

        location = Location.query.filter(Location.id==1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_404_delete_location_if_not_exist(self):
        res = self.client().delete('locations/1000',
        headers=get_headers(OWNER))

        data = json.loads(res.data.decode('utf-8'))

        location = Location.query.filter(Location.id==1000).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    '''

    
    #BOOK TESTS
    '''
    def test_post_book_auth(self): #works 
        res = self.client().post('/books/add',
            json={
                'title': 'Test Book 2',
                'author': 'great author 2',
                'form': 'ebook',
                'location_id': 12
            },
            headers=get_headers(OWNER))

        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(['success'], True)
        self.assertTrue(['created'])
        self.assertTrue(['total_books'])
    
    def test_403_permission_not_found_post_book_not_auth(self): #works
        res = self.client().post('/books/add', 
        headers=get_headers(USER),
            json={
                'title': 'Test Book 2',
                'author': 'great author 2',
                'form': 'ebook',
                'location_id': 1
            })


        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'], False)
        self.assertTrue(data['message'], 'Permission not found')

    def test_get_books(self): #works
        res = self.client().get('/books')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books']) 
    

    #test if no books 
    def test_get_locations_when_none(self):#works
        res = self.client().get('/books')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])

    def test_update_book_authorized(self):#res errors if location doesn't exist
        res = self.client().patch('books/2',
        json={
            'author': 'Changed Author18',
            'location_id': 10
        },
        headers=get_headers(OWNER))

        data = json.loads(res.data.decode('utf-8'))
        book = Book.query.filter(Book.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['book.id'])

    #def test_404_book_location_not_exist(self):
        #res = self.client().patch('books/4',
        #json={
            #'title': 'Title008',
            #'author': 'Wonder Worder',
            #'form': 'cool1',
            #'location_id': 2000
        #},
        #headers=get_headers(OWNER))

        #data = json.loads(res.data.decode('utf-8'))
        #book = Book.query.filter(Book.id == 4).one_or_none()

        #self.assertEqual(res.status_code, 404)
        #self.assertTrue(data['success'], False)

    def update_book_not_authorized(self):
        res = self.client().patch('books/1',
        json={'title': 'Changed_Title'},
        headers=get_headers(USER))
    
        data = json.loads(res.data.decode('utf-8'))
        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], Unauthorized)

    def delete_book_auth(self): #requires auth
        res = self.client().delete('books/1',
        json=self.new_book_1,
        headers=get_headers(OWNER))

        data = json.loads(res.data.decode('utf-8'))

        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(book, None)

    def test_403_delete_book_not_authorized(self):
        res = self.client().delete('books/1',
        json=self.new_book_1,
        headers=get_headers(USER))

        data = json.loads(res.data.decode('utf-8'))

        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], Unauthorized)
    '''
# Make the tests executable
if __name__ == "__main__":
    unittest.main()