import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
#?create_app; Trivia has def create_app
from models import setup_db, Location, Book
from dotenv import load_dotenv

load_dotenv() #loads environment variables

#assigning env variables
USER = os.environ.get('user_jwt')
OWNER = os.environ.get('owner_jwt')

def get_headers(token):
    return {'Authorization': f'Bearer {token'}

#???app = Flask(__name__)
#API Testing 4.2

class StuffTestCase(unittest.TestCase):
    def setUp(self):#from bookshelf I think
        """Executed before each test. Define test variables and initialize app."""
        self.app = create_app()###need create_app function in app.py
        self.client = app.test_client
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
        self.new_book = {
            "title": "Title1", 
            "author": "Author1", 
            "form": "ebook",
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
    
    #def test_post_location_not_auth(self)



    def test_get_location(self):
        res = self.client().get('/locations')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['locations'])
        self.assertTrue(data['number of locations'])

    #test if no locations found
    
    #With authorizations
    def test_update_location_authorized(self): #payload
        res = self.client().patch('locations/1', json={'name': 'upshelf'})
        data = json.loads(res.data)
        location = Location.query.filter(Location.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['location.id'])

    #def test_update_location_not_auth

        #self.assertEqual(res.status_code, 422)

    #def delete_location_auth
    
    
    #def delete_location_not_auth

        #self.assertEqual(res.status_code, 422)

    #BOOK TESTS
    def test_post_book_auth(self): # + location
        res = self.client().post('/books/add')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(['success'], True)
        self.assertTrue(['created'])
        self.assertTrue(['total_books'])

    #def test_post_book_not_auth(self): # + location

        #self.assertEqual(res.status_code, 422)
    def test_get_books(self): #no auth ndd
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success', True])
        self.assertTrue(data(['total_books']))

    #test if no books found
    
    #def update_book_auth(self)

        #self.assertEqual(res.status_code, 422)

    #def update_book_not_auth(self)
    

        #self.assertEqual(res.status_code, 422)
    #def delete_book_auth(self)

        #self.assertEqual(res.status_code, 200)
    
    #def delete_book_not_auth(self)

        #self.assertEqual(res.status_code, 422)




    
    









# Make the tests conveniently executable
if __name__ == "__main__":
unittest.main()