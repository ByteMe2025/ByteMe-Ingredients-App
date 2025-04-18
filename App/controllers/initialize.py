from .user import create_user
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')

def get_recipes():
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({error: 'Failed to fetch recipes'}), 500
