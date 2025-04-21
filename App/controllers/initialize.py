from flask import jsonify
from .user import create_user
from sqlite3 import IntegrityError
from App.database import db
from App.models import Recipe, Ingredient, RecipeIngredients
import requests

def initialize():
    db.drop_all()
    db.create_all()
    create_user("bob", "bobpass")
    api_call()

def api_call():
    url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=dcd0266fa29a472f9bc5245206a24923&number=2&instructionsRequired=true&addRecipeInformation=true'
    try:
        response = requests.get(url)
        data = response.json()
        for recipe in data['results']:
            for instruction in recipe.get('analyzedInstructions', []):
                for step in instruction.get('steps', []):
                    rec = Recipe(
                        id = recipe['id'],
                        title=recipe['title'],
                        image=recipe['image'],
                        ready_in_mins=recipe['readyInMinutes'],
                        servings=recipe['servings'],
                        health_score=recipe['healthScore'],
                        price_per_serving=recipe['pricePerServing'],
                        cheap =recipe['cheap'],
                        dish_type = recipe['dishTypes'][0]
                        )
                    db.session.add(rec)
                    
                    for ingredient in step.get('ingredients', []):
                        if not Ingredient.query.filter_by(name=ingredient['name']).first():
                            ing = Ingredient(
                                name = ingredient['name'],
                                image = ingredient['image'],
                            )
                            db.session.add(ing)
                            db.session.commit()
                            rec_ing = RecipeIngredients(recipe_id=rec.id, ingredient_id=ing.id)
                            db.session.add(rec_ing)
        db.session.commit()
    except IntegrityError:
        return jsonify('message: Failed to fetch recipes'), 500

def print_recipe():
    for recipe in Recipe.query.all():
        print(recipe.title)
        print(recipe.image)
        print(recipe.ready_in_mins)
        print(recipe.servings)
        print(recipe.health_score)
        print(recipe.price_per_serving)
        print(recipe.cheap)
        print(recipe.dish_type)
        print('-------------------')

def print_ingredient():
    for ingredient in Ingredient.query.all():
        print(ingredient.name)
        print(ingredient.image)
        print('-------------------')