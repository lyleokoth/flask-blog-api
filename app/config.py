import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = 'secret_key'
    DEBUG = False
    TESTING = False 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESULTS_PER_PAGE = 10

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('app-development.db')

class ProductionConfig(BaseConfig):
    SECRET_KEY = 'another_secret_key'
    DEBUG = False
    TESTING = False 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('app-production.db')