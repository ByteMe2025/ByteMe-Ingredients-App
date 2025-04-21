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
    # backup API key: dcd0266fa29a472f9bc5245206a24923
    # backup API key: 1ce7256217df44ba94585d99e4853796
    # backup API key: 4e3b2fc12a714940b03ae344ab792f2d
    url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=98826ec574794926ba76b7bdaefaa7c0&number=14&instructionsRequired=true&addRecipeInformation=true&addRecipeInstructions=true'
    try:
        response = requests.get(url)
        data = response.json()
        for recipe in data['results']:
            instructions = ''
            rec = Recipe(
                id = recipe['id'],
                title=recipe['title'],
                image=recipe['image'],
                ready_in_mins=recipe['readyInMinutes'],
                servings=recipe['servings'],
                health_score=recipe['healthScore'],
                price_per_serving=recipe['pricePerServing'],
                cheap =recipe['cheap'],
                dish_type = recipe['dishTypes'][0],
                instructions = instructions
            )
            db.session.add(rec)

            for instruction in recipe.get('analyzedInstructions', []):
                for step in instruction.get('steps', []):
                    instructions += str(step['number']) + '. ' + step['step'] + '\n'

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
                rec.updateInstructions(instructions)
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