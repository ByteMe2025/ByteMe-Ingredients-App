from .models import *
from .views import *
from .controllers import *
from .main import *
import os

def display_recipe_ingredients(recipeID):
    owned_ings = []
    missing_ings = []
    recipe_ingredients = RecipeIngredients.query.filter_by(recipe_id=recipeID).all()

    for recipe_ingredient in recipe_ingredients:
        user_ingredient = UserIngredients.query.filter_by(user_id=current_user.id, ingredient_id=recipe_ingredient.ingredient_id).first()
        if user_ingredient:
            owned_ings.append(user_ingredient.ingredient.name)
        else:
            missing_ings.append(recipe_ingredient.ingredient.name)
    return owned_ings, missing_ings


def show_recipe_instructions(recipeID):
    recipe = Recipe.query.get(recipeID)
    user_recipes = UserRecipes.query.all()
    recipes = Recipe.query.all()

    ings_per_rec = {}
    for user_recipe in user_recipes:
        owned, missing = display_recipe_ingredients(user_recipe.recipe_id)
        ings_per_rec[user_recipe.recipe_id] = {
            'owned': owned,
            'missing': missing
        }

    if not recipe:
        flash('Recipe not found')
        return redirect(url_for('index_views.home_page'))
    else:
        url = f'https://api.spoonacular.com/recipes/{recipeID}/analyzedInstructions?apiKey=dcd0266fa29a472f9bc5245206a24923'
        try:
            response = requests.get(url)
            data = response.json()
            instructions = []
            for step in data[0]['steps']:
                instructions.append(step['step'])
            return render_template('index.html', recipes=recipes, user_recipes=user_recipes, current_user=current_user, instructions=instructions, recipe=recipe, ings_per_rec=ings_per_rec)
        except IntegrityError:
            flash('Failed to fetch recipe instructions')
            return redirect(url_for('index_views.home_page'))


@index_views.route('/updatedHome/<id>', methods=['GET'])
@jwt_required()
def updatedHome_page(id):
    return show_recipe_instructions(id)
    

@index_views.route('/signup', methods=['POST'])
def register_user():
    data = request.form
    newUser = create_user(data['username'], data['password'])
    if newUser:
        flash('User created successfully')
        return redirect(url_for('index_views.login_page'))
    else:
        return redirect(url_for('index_views.register_page'))
    
@index_views.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@index_views.route('/home', methods=['GET'])
@jwt_required()
def home_page():
    user_recipes = UserRecipes.query.all()
    recipes = Recipe.query.all()
    user_ingredients = UserIngredients.query.all()

    ings_per_rec = {}
    for user_recipe in user_recipes:
        owned, missing = display_recipe_ingredients(user_recipe.recipe_id)
        ings_per_rec[user_recipe.recipe_id] = {
            'owned': owned,
            'missing': missing
        }

    return render_template('dashboard.html', user_ingredients=user_ingredients, recipes=recipes, user_recipes=user_recipes, current_user=current_user, ings_per_rec=ings_per_rec)

@auth_views.route('/addIngredient/<id>', methods=['POST'])
@jwt_required()
def add_ingredient(id):
    amount = request.form
    ingredient = Ingredient.query.get(id)
    user_ingredient = UserIngredients.query.filter_by(user_id=current_user.id, ingredient_id=id).first()
    if user_ingredient: 
        flash('Ingredient already owned')
        user_ingredient.update_amount(float(amount['amount']))
        flash('Ingredient amount updated')
        return redirect(url_for('auth_views.show_ingredients'))
    else: 
        ingredient.add_ingredient_to_user(current_user.id, amount['amount'])
        flash('Ingredient added to user')
        return redirect(url_for('auth_views.show_ingredients'))

@auth_views.route('/ingredients', methods=['GET'])
@jwt_required()
def show_ingredients():
    #user_ingredients = UserIngredients.query.all()
    ingredients = Ingredient.query.all()
    return render_template('ingredients.html', ingredients=ingredients)

@auth_views.route('/recipes', methods=['GET'])
@jwt_required()
def show_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)


@auth_views.route('/addFavrecipe/<id>', methods=['POST'])
@jwt_required()
def add_fav_recipe(id):
    recipe = Recipe.query.get(id)
    user_recipe = UserRecipes.query.filter_by(recipe_id=id).first()
    if user_recipe: 
        flash('Recipe already favorited')
        return redirect(url_for('auth_views.show_recipes'))
    else: 
        recipe.add_fav_recipe_to_user(current_user.id)
        flash('Recipe added to user')
        return redirect(url_for('auth_views.show_recipes'))

@auth_views.route('/removeIngredient/<id>', methods=['POST'])
@jwt_required()
def remove_ingredient(id):
    user_ingredient = UserIngredients.query.get(id)
    if not user_ingredient: 
        flash('Ingredient not found')
        return redirect(url_for('index_views.home_page'))
    else:
        user_ingredient.remove_ingredient_from_user(current_user.id)
        flash('Ingredient removed from user')
        return redirect(url_for('index_views.home_page'))

@auth_views.route('/removeFavrecipe/<id>', methods=['POST'])
@jwt_required()
def remove_fav_recipe(id):
    user_recipe = UserRecipes.query.get(id)
    if not user_recipe: 
        flash('Recipe not found')
        return redirect(url_for('index_views.home_page'))
    else:
        user_recipe.remove_fav_recipe_from_user(current_user.id)
        flash('Recipe removed from user')
        return redirect(url_for('index_views.home_page'))




@index_views.route('/api_call', methods=['GET'])
def api_call():
    url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=dcd0266fa29a472f9bc5245206a24923&number=1&instructionsRequired=true&addRecipeInformation=true&addRecipeInstructions=true'
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except IntegrityError:
        return jsonify('message: Failed to fetch recipes'), 500