from .user import create_user
from App.database import db
from App.views.index import api_call


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    api_call()
