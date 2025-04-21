from .user import *

class Ingredient (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False, unique = True) 
    image = db.Column(db.String(120), nullable = True)
    recipes = db.relationship('RecipeIngredients', backref='ingredient', lazy=True)
    users = db.relationship('UserIngredients', backref='ingredient', lazy=True)

    def __init__(self, name, image):
        self.name = name 
        self.image = image

    def add_ingredient_to_user(self, userID, amount):
        userIngredient = UserIngredients(userID, self.id, amount)
        db.session.add(userIngredient)
        db.session.commit()

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
    instructions = db.Column(db.Text, nullable = True)
    ingredients = db.relationship('RecipeIngredients', backref='recipe', lazy=True)
    users = db.relationship('UserRecipes', backref='recipe', lazy=True)

    def __init__(self, id, title, image, servings, ready_in_mins, health_score, price_per_serving, cheap, dish_type):
        self.id = id
        self.title = title
        self.image = image
        self.servings = servings
        self.ready_in_mins = ready_in_mins
        self.health_score = health_score
        self.price_per_serving = price_per_serving
        self.cheap = cheap
        self.dish_type = dish_type

      
    def add_fav_recipe_to_user(self, user_id):
        userRecipe = UserRecipes(user_id, self.id)
        db.session.add(userRecipe)
        db.session.commit()

    def updateInstructions(self, instructions):
        self.instructions = instructions
        db.session.commit()

class UserRecipes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), nullable = False)

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id

    def remove_fav_recipe_from_user(self, userID):
        userRecipe = UserRecipes.query.filter_by(user_id=userID, id=self.id).first()
        if userRecipe:
            db.session.delete(userRecipe)
            db.session.commit()

class UserIngredients(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(Ingredient.id), nullable = False)
    amount = db.Column(db.Float, nullable = False)

    def __init__(self, user_id, ingredient_id, amount):
        self.user_id = user_id
        self.ingredient_id = ingredient_id
        self.amount = amount

    def remove_ingredient_from_user(self, user_id):
        userIngredient = UserIngredients.query.filter_by(id=self.id, user_id=user_id).first()
        if userIngredient:
            db.session.delete(userIngredient)
            db.session.commit()

    def update_amount(self, new_amount):
        self.amount = self.amount + new_amount
        db.session.commit()

class RecipeIngredients(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), nullable = False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(Ingredient.id), nullable = False)

    def __init__(self, recipe_id, ingredient_id):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id