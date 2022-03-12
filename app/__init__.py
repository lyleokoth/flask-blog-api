from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
if os.environ['FLASK_ENV'] == 'production':
    print(os.environ['FLASK_ENV'])
    app.config.from_object(ProductionConfig)

db = MongoEngine(app)

from app import routes, models