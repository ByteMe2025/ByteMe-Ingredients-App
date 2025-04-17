from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    recipes = db.relationship('UserRecipes', backref='user', lazy=True)
    ingredients = db.relationship('UserIngredients', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Ingredient (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False, unique = True) 
    amount = db.Column(db.Float, nullable = False)
    image = db.Column(db.String(120), nullable = True)
    recipes = db.relationship('RecipeIngredients', backref='ingredients', lazy=True)

    def __init__(self, name, amount, image):
        self.name = name 
        self.amount = amount
        self.image = image 

    
class Recipe (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False, unique = True)
    image = db.Column(db.String(120), nullable = True)
    servings = db.Column(db.Integer, nullable = False)
    ready_in_mins = db.Column(db.Integer, nullable = False)
    health_score = db.Column(db.Float, nullable = False)
    price_per_serving = db.Column(db.Float, nullable = False)
    cheap = db.Column(db.Boolean, nullable = False)
    dish_type = db.Column(db.String(80), nullable = False)

    def __init__(self, title, image, servings, ready_in_mins, health_score, price_per_serving, cheap, dish_type):
        self.title = title
        self.image = image
        self.servings = servings
        self.ready_in_mins = ready_in_mins
        self.health_score = health_score
        self.price_per_serving = price_per_serving
        self.cheap = cheap
        self.dish_type = dish_type