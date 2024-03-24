# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication
from games.authentication.authentication import login_required
import games.utilities.services as util
# ---------------------------------------

import games.genre_bases.services as services
from games.domainmodel.model import *
genre_bases_blueprint = Blueprint("genre_bases_bp", __name__)

games_per_page = 30

order_g = None
pagenum_g = None
genre_g = None

@genre_bases_blueprint.route('/genre/<target>', methods=["GET"])
def show_games(target=None,reflesh=None):
    # check if authenticated
    authenticated = authentication.check_authenticated()
    
    pagenum = request.args.get("page")
    order = request.args.get("order")
    
    genres_list = services.get_genre_list(repo.repo_instance)
    
    if(reflesh!=True):
        if not order:
            order =""
        
        #if pagenum is not set then page is 1 else page is given value for invalid page
        if not pagenum:
            pagenum = 1
        else:
            try:
                pagenum = int(pagenum)
            except:
                return render_template("notFound.html", message=f"Invalid page value!")
            
        for _genre in genres_list:
            if(_genre.genre_name == target):
                genre = _genre

        global order_g, pagenum_g, genre_g
        order_g = order
        pagenum_g = pagenum
        genre_g = genre
    
    else:
        order = order_g
        pagenum = pagenum_g
        genre = genre_g

    services.get_games_by_genre(repo.repo_instance,genre)
    favourite_list = []
    if "User_name" in session:
        user_name = session["User_name"]
        favourite_list = services.get_favourite_list(repo.repo_instance,user_name)

    num_games = services.get_number_of_games(repo.repo_instance)
    games = services.get_games(repo.repo_instance, games_per_page, pagenum, order)
    maxpage = services.get_max_page_num(num_games, games_per_page)
    pages = services.generate_page_list(pagenum, maxpage)
    option_of_order = ["game_id", "title", "publisher", "release_date", "price"]

    page_info = {
        "number_of_games": num_games,
        "maxpage": maxpage,
        "current_display": services.get_current_display(num_games, games_per_page, pagenum),
        "current_page": pagenum,
        "current_order": order
    }
    
    return render_template(
        "genre.html",
        games=games,
        num_game=num_games,
        page_info=page_info,
        pages=pages,
        order_options=option_of_order,
        genres=genres_list,
        genre=genre,
        authenticated=authenticated,
        favourite_list=favourite_list
    )

@genre_bases_blueprint.route("/genre/change_favourite/<game_id>")
@login_required
def change_favourite(game_id: str):
    user_name = None
    if "User_name" in session:
        user_name = session["User_name"]
        try:
            util.change_favourite(repo.repo_instance,(game_id),user_name)
        except: # if game not found
            geners_list = services.get_genre_list(repo.repo_instance)
            authenticated = authentication.check_authenticated()
            return render_template(
                "notFound.html",
                message=f"game id: {game_id} is not found.",
                genres=geners_list,
                authenticated=authenticated
            )
    else:
        pass
    return show_games(None,True)

