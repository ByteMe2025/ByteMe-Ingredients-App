from .models import *
from .views import *
from .controllers import *
from .main import *
import os


@index_views.route('/home', methods=['GET'])
def home_page():
    user_recipes = UserRecipes.query.all()
    user_ingredients = UserIngredients.query.all()
    return render_template('index.html', user_recipes=user_recipes, user_ingredients=user_ingredients)

@auth_views.route('/addIngredient/<id>', methods=['POST'])
@jwt_required()
def add_ingredient(id):
    amount = request.form
    ingredient = Ingredient.query.get(id)
    if not ingredient: 
        flash('Ingredient not found')
        return redirect(url_for('auth_views.show_ingredients'))
    else: 
        ingredient.add_ingredient_to_user(current_user.id, id, amount['amount'])
        flash('Ingredient added to user')
        return redirect(url_for('auth_views.show_ingredients'))

@auth_views.route('/ingredients', methods=['GET'])
@jwt_required()
def show_ingredients():
    ingredients = Ingredient.query.all()
    return render_template('ingredients.html', ingredients=ingredients)

@auth_views.route('/addFavrecipe/<id>', methods=['POST'])
def add_fav_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe: 
        flash('Recipe not found')
        return redirect(url_for('auth_views.show_recipes'))
    else: 
        current_user.add_fav_recipe_to_user(current_user.id, id)
        flash('Recipe added to user')
        return redirect(url_for('auth_views.show_recipes'))

@auth_views.route('/recipes', methods=['GET'])
def show_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@auth_views.route('/removeIngredient/<id>', methods=['POST'])
def remove_ingredient(id):
    ingredient = Ingredient.query.get(id)
    if not ingredient: 
        flash('Ingredient not found')
        return redirect(url_for('auth_views.show_ingredients'))
    else:
        current_user.remove_ingredient_from_user(current_user.id, id)
        flash('Ingredient removed from user')
        return redirect(url_for('auth_views.show_ingredients'))

@auth_views.route('/removeFavrecipe/<id>', methods=['POST'])
def remove_fav_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe: 
        flash('Recipe not found')
        return redirect(url_for('auth_views.show_recipes'))
    else:
        current_user.remove_fav_recipe_from_user(current_user.id, id)
        flash('Recipe removed from user')
        return redirect(url_for('auth_views.show_recipes'))

""" @index_views.route('/api_call', methods=['GET'])
def api_call():
    url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=1ce7256217df44ba94585d99e4853796&number=1&instructionsRequired=true&addRecipeInformation=true'
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except IntegrityError:
        return jsonify('message: Failed to fetch recipes'), 500 """