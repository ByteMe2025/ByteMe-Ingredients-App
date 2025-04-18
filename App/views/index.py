from sqlite3 import IntegrityError
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for
from App.controllers import create_user, initialize
import requests

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def init_route():
    initialize()
    return redirect(url_for('index_views.login_page'))

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/home', methods=['GET'])
def home_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/api_call', methods=['GET'])
def api_call():
    url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=1ce7256217df44ba94585d99e4853796&number=1&instructionsRequired=true&addRecipeInformation=true'
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except IntegrityError:
        return jsonify('message: Failed to fetch recipes'), 500


