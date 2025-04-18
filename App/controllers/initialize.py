from .user import create_user
from App.database import db
from App.views.index import api_call


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    from App.views.index import api_call  # Local import to avoid circular dependency
    api_call()
