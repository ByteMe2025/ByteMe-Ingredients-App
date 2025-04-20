from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models import UserIngredients, UserRecipes

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

    def add_ingredient_to_user(self, ingredientID, amount):
        userIngredient = UserIngredients(self.id, ingredientID, amount)
        db.session.add(userIngredient)
        db.session.commit()

    def add_fav_recipe_to_user(self, recipeID):
        userRecipe = UserRecipes(self.id, recipeID)
        db.session.add(userRecipe)
        db.session.commit()
    
    def remove_ingredient_from_user(self, ingredientID):
        userIngredient = UserIngredients.query.filter_by(user_id=self.id, ingredient_id=ingredientID).first()
        if userIngredient:
            db.session.delete(userIngredient)
            db.session.commit()

    def remove_fav_recipe_from_user(self, recipeID):
        userRecipe = UserRecipes.query.filter_by(user_id=self.id, recipe_id=recipeID).first()
        if userRecipe:
            db.session.delete(userRecipe)
            db.session.commit()

