## Where's My Stuff?
A place to hold where stuff is

### Installation of Development Environment
python 3.7

* `python3 -m venv env` set the virtual environment for Pyhton 
* `source venv/bin/activate` activate the virtual environment
* `python -m pip install -r requirements.txt` to install dependencies. All required packages are included in the requirements file. 
* `deactivate` - de-activates the virtual environment


### API documentation

#### Backend



	
#### Connect Postgres Database
After your first install, and each time you restart your machine you will have to also restart the postgres service, or else you will get an operational error. (Is the server running?)
	1. To start the service, type ```sudo service postgresql start```
	2. To connect to postgres, type ```sudo -u postgres psql```
	
You should get a prompt asking for your password. If this doesn't work, then you can try the second option listed below.
	1. Switch users to postgres by typing su - postgres
	2. Type psql.
When this is successful you will see the command line change to look like this postgres=#

Connect to stuff database with
``` \c stuff ```

Other postgres commands are: 
\c <db_name> - connects to <db_name>
\l - lists tables
\dt - list of relations
\d <table/relation_name> - lists columns

Stop the PostgreSQL server:
```sudo service postgresql stop```


#### Invoke app from CLI:
```python 
export FLASK_APP=app.py
export FLASK_DEBUG=true
flask run
```

README from todoapp-crud-lists-soln
# SAMPLE VERSION OF TODO APP
This app is written in Python with Flask and SQLAlchemy, as a part of the Udacity's Full Stack Web Developer Nanodegree program.

## A. Dependency
In order to run this app, the following dependencies must have been already installed:
1. Postgres. 
 * Start manually: `pg_ctl -D /usr/local/var/postgres start`
 * Stop manually: `pg_ctl -D /usr/local/var/postgres stop -s -m fast`
 
2. Flask

#TODO ## B. Database 
The database relations `todos(id, description, complete, list_id)` and `todolists(id, name)` must have been already created in Postgres. We have assumed that the Postgres is running on default port 5432.

* `dropdb todoapp -p 5432 && createdb todoapp -p 5432` 
* Open the database prompt - `psql -p 5432`
* Connect to the database - `\c todoapp` 
* Displays the tables in the database `\dt` 
* Displays the schema of the 'todos' table `\d todos` 
* Displays the schema of the 'todolists' table `\d todolists` 

You can insert a few rows in both the tables. Insert first in the `todolists` relation. 


## C. Steps to Run the App: 
* `python3 -m venv env` set the virtual environment for Pyhton 
* `source venv/bin/activate` activate the venv
* `python -m pip install -r requirements.txt` to install dependencies. For Mac users, if you face difficulty in installing the `psycopg2`, you may consider intalling the `sudo brew install libpq` before running the `requirement.txt`. 
* `python3 app.py` to run the app (http://127.0.0.1:5000/ or http://localhost:5000)
* `deactivate` - de-activates the virtual environment




