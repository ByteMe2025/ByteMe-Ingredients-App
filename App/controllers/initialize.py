from flask import jsonify
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

def api_call():
    url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=1ce7256217df44ba94585d99e4853796&number=1&instructionsRequired=true&addRecipeInformation=true'
    try:
        response = requests.get(url)
        data = response.json()
        for recipe in data['results']:
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

            for instruction in recipe.get('analyzedInstructions', []):
                for step in instruction.get('steps', []):
                    for ingredient in step.get('ingredients', []):
                        ing = Ingredient(
                            id = ingredient['id'],
                            name = ingredient['name'],
                            image = ingredient['image'],
                        )  
                        db.session.add(ing)
        db.session.commit()
        print_recipe()
        print_ingredient()
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