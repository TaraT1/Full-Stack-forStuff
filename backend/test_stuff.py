import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Location, Book

#API Testing 4.2

class LocationTestCase(unittest.TestCase):
    """This class represents a stuff test case"""

    def setUp(self):
        """Executed before each test. Define test variables and initialize app."""
        self.app = create_app()
        self.client = app.test_client
        self.database_name = "test_db"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        #create new location record for testing
        self.new_location = {
            "name": "shelf ds1",
            "type": "bookshelf"
        }

    
        self.new_book = {
            "title": "Title1", 
            "author": "Author1", 
            "form": "ebook_kindle",
            "location_id": 2
        }

        #bind app to current context
        with self.app.app_context():
            self.db = SQLAlchemy
            self.db.init_app(self.app)
            #create tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

        #LOCATION TESTS
        #def post_location

        #def get_location

        #def update_location

        #def delete_location


        #BOOK TESTS
        #def post_book, location

        #def get_book

        

        #def delete_book

    












# Make the tests conveniently executable
if __name__ == "__main__":
unittest.main()