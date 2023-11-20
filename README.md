# Project 12 of the OpenClassrooms Python developper training

## develop a secure back-end with python and SQL

This project aims to develop a back-end using python and SQL
It uses sqlalchemy as orm and can connect to sqlite, mysql and postgres databases
It uses the MVC pattern and provide a view for CLI using Rich

## Installation

### Sources

In order to run the application, clone the following repository in the directory where you want the application to be stored : https://github.com/chpancrate/ocrpy_project12


### Environment setup 

The application runs with Python 3.11.

To install python you can download it here : https://www.python.org/downloads/

If you are new to Python you can find information here : https://www.python.org/about/gettingstarted/ 

It is better to run the application in a virtual environment. You can find information on virtual envrionments here : https://docs.python.org/3/library/venv.html 

Once in your virtual environment, the following modules are mandatory :
- Django : 4.2.3
- djangorestframework : 3.14.0
- djangorestframework-simplejwt : 5.2.2

All the useful modules are in the requirements.txt file. A quick way to install them is to run the command below in a python terminal:
```
pip install -r requirements.txt
```

## How to run the API

In order to run the application once the setup is complete go in the directory where the application is installed and then use the command : 
```
python manage.py runserver
```
