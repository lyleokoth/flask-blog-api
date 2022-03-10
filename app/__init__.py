from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = MongoEngine(app)

from app import routes, models