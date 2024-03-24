# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication
import games.utilities.services as util
from games.authentication.authentication import login_required

# ---------------------------------------
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import games.game_desc.services as services
game_desc_blueprint = Blueprint("game_desc_bp", __name__)

@game_desc_blueprint.route('/gameDescription/<game_id>', methods=["GET"])
def game_description(game_id):
    # check if authenticated
    authenticated = authentication.check_authenticated()
    
    game = None
    geners_list = services.get_genre_list(repo.repo_instance)
    
    try:
        # check that recived value is integer
        game_id = int(game_id)
        game = services.get_game(repo.repo_instance, game_id)
    except: # if game not found
        return render_template(
            "notFound.html",
            message=f"game id: {game_id} is not found.",
            genres=geners_list,
            authenticated=authenticated
        )
        
    else: # if not error
        review_list = services.get_user_review(repo.repo_instance, game_id)
        favourite_list = False
        if "User_name" in session:
            user_name = session["User_name"]
            favourite_list = services.get_favourite_list(repo.repo_instance,game_id,user_name)
        return render_template(
            'gameDescription.html',
            game=game,
            genres=geners_list,
            authenticated=authenticated,
            review_list=review_list,
            favourite_list = favourite_list
        )
    

@game_desc_blueprint.route('/review/<game_id>/<rate>/<comment>', methods=["GET"])
@login_required
def review(game_id: int, rate: int, comment: str):
    user_name = None
    if "User_name" in session:
        user_name = session["User_name"]
                
        # print(review)
        try:
            if (6> int(rate) > 0 and services.get_game(repo.repo_instance,int(game_id))!=None and comment!="style.css"):
                #get game 
                services.review(repo.repo_instance,int(game_id),int(rate),comment,user_name)
                
                return redirect(url_for('game_desc_bp.game_description', game_id=game_id))
            else:
                return redirect(url_for('game_desc_bp.game_description', game_id=game_id))
        except:
            return redirect(url_for('game_desc_bp.game_description', game_id=game_id))
        
    else :
        return redirect(url_for('game_desc_bp.game_description', game_id=game_id))


@game_desc_blueprint.route("/gameDescription/change_favourite/<game_id>")
@login_required
def change_favourite(game_id: str):
    user_name = None
    if "User_name" in session:
        user_name = session["User_name"]
        #if (services.get_game(repo.repo_instance,int(game_id))!=None):
        try:
            services.change_favourite(repo.repo_instance,(game_id),user_name)
        except: # if game not found
            geners_list = services.get_genre_list(repo.repo_instance)
            authenticated = authentication.check_authenticated()
            return render_template(
                "notFound.html",
                message=f"game id: {game_id} is not found.",
                genres=geners_list,
                authenticated=authenticated
            )          
    return redirect(url_for('game_desc_bp.game_description', game_id=game_id))

class ReviewForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired()])
    rate = HiddenField("Rating")
    submit = SubmitField('Submit')