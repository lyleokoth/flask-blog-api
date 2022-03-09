from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate