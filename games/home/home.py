# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication

# ---------------------------------------

home_blueprint = Blueprint("home_bp", __name__)


@home_blueprint.route('/', methods=['GET'])
@home_blueprint.route("/home", methods=['GET'])
def home():
    # check if authenticated
    authenticated = authentication.check_authenticated()
    message = getmessage()
    
    # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    genres_list = repo.repo_instance.get_genre_list()
    return render_template(
        "home.html",
        genres=genres_list,
        authenticated=authenticated,
        message=message
    )
    
    
def getmessage() -> str:
    if "User_name" in session:
        return f"Hello {session['User_name']}, welcome back."
    else:
        return "You are not loged in. Please login or register to use all features."
        
