# Project 12 of the OpenClassrooms Python developper training

## develop a secure back-end with python and SQL

This project aims to develop a back-end using python and SQL.

It uses sqlalchemy as ORM and can connect to sqlite, mysql and postgresql databases. The connection to mysql uses pymysql. 

The database migrations are handled with alembic.

It uses the MVC pattern and provide a view for a Command Line Interface using Rich.

Json Web Yoken are used to ensure authentification and are managed with the package pyjwt.

The password are hashed using argon2-cffi.

Run supervision is enabled with sentry.

## Installation

### Sources

In order to run the application, clone the following repository in the directory where you want the application to be stored : https://github.com/chpancrate/ocrpy_project12


### Environment setup 

The application runs with Python 3.11.

To install python you can download it here : https://www.python.org/downloads/

If you are new to Python you can find information here : https://www.python.org/about/gettingstarted/ 

It is better to run the application in a virtual environment. You can find information on virtual envrionments here : https://docs.python.org/3/library/venv.html 

Once in your virtual environment, the following modules are mandatory to run the application :
- alembic==1.12.1
- argon2-cffi==23.1.0
- PyJWT==2.8.0
- PyMySQL==1.1.0
- rich==13.7.0
- sentry-sdk==1.9.0
- SQLAlchemy==2.0.23

In order to run the test files you need to install :
- pytest==7.4.3

All the useful modules are in the requirements.txt file. A quick way to install them is to run the command below in a python terminal:
```
pip install -r requirements.txt
```

### .env file
Several parameters need to be setup in the file .env at the root of the project.

- DB_ENGINE = declare the database engine to be used : mysql, sqlite, postgresql., test (allow to point to a test database using sqllite for automated test purpose).

The following database connection information must be set :
- DB_USER = user to be used to acces the DB
- DB_PASS = password of the user
- DB_HOST = host of the DB (example 'localhosts')
- DB_NAME = name of the DB

The json web token configuration is :
- SECRET_KEY = secret key to be used for token encryption
- ACCESS_TOKEN_DELAY = an integer in minutes, validity duration for acces token 
- REFRESH_TOKEN_DELAY = an integer in minutes, vlidity duration for refresh token

The sentry configuration is 
- SENTRY_DSN = dsn link to your sentry project

To learn more about sentry setup please follow the link : https://docs.sentry.io/platforms/python/

### Database set-up

In order to run the application you need to create the database structure. Once your database is created and you have filled the .env file. You can create the tables in the Database by using alembic: 
```
alembic upgrade heads
```

## Application launch
To setup the minimal needed data and create the first user (admin user) run the script db_initialization.py :
```
python db_initialization.py
```
Be sure to update the password in the file first and then erase it from the file once used.

In order to launch the application use the command :

```
python epicevents.py
```
Using the admin account you can create the other users account.