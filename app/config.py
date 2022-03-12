import os
import bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = 'secret_key'
    DEBUG = False
    TESTING = False 
    SALT = bcrypt.gensalt()

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MONGODB_DB = 'flask-api'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_USERNAME = ''
    MONGODB_PASSWORD = ''
    MONGODB_CONNECT = True

class ProductionConfig(BaseConfig):
    SECRET_KEY = 'another_secret_key'
    DEBUG = False
    TESTING = False 
    MONGODB_DB = 'flask-api'
    MONGODB_HOST = 'mongodb+srv://cluster0.ctzy7.mongodb.net/'
    MONGODB_PORT = 27017
    MONGODB_USERNAME = 'flask-api'
    MONGODB_PASSWORD = 'flask-api'
    MONGODB_CONNECT = True