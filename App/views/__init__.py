# blue prints are imported 
# explicitly instead of using *
from sqlite3 import IntegrityError
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_jwt_extended import current_user, jwt_required
import requests

from App.models import Ingredient, Recipe
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin


views = [user_views, index_views, auth_views] 
# blueprints must be added to this list

