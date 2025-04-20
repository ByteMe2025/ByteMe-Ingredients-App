from flask import jsonify

from App.controllers import api_call
from .user import create_user
from sqlite3 import IntegrityError
from App.database import db
from App.models import Recipe, Ingredient
import requests

def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    api_call()
