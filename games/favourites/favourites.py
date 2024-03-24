from flask import Blueprint, render_template, request, session, redirect, url_for
# from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.authentication.authentication import login_required

import games.adapters.repository as repo
import games.favourites.services as services
import games.authentication.authentication as authentication
import games.utilities.services as util
favourites_blueprint = Blueprint("favourites_bp", __name__)

games_per_page = 10

order_c = None
pagenum_c = None

@favourites_blueprint.route('/favourites', methods=['GET'])
@login_required
def show_games(reflesh=None):
    authenticated = authentication.check_authenticated()
    user_name = session["User_name"]
    pagenum = request.args.get("page")
    order = request.args.get("order")
    
    if(reflesh==None):
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
        global order_c, pagenum_c
        order_c = order
        pagenum_c = pagenum
    
    else:
        order = order_c
        pagenum = pagenum_c
        
    
    num_games = services.get_number_of_games(repo.repo_instance, user_name)
    games = services.get_games(repo.repo_instance, games_per_page, pagenum, user_name, order)
    maxpage = services.get_max_page_num(num_games, games_per_page)
    pages = services.generate_page_list(pagenum, maxpage)
    option_of_order = ["game_id", "title", "publisher", "release_date", "price"]
    geners_list = services.get_genre_list(repo.repo_instance)
    
    page_info = {
        "number_of_games": num_games,
        "maxpage": maxpage,
        "current_display": services.get_current_display(num_games, games_per_page, pagenum),
        "current_page": pagenum,
        "current_order": order
    }
    
    return render_template("favourites.html", games=games, num_game=num_games, page_info=page_info, pages=pages, order_options=option_of_order,genres=geners_list,authenticated=authenticated)

@favourites_blueprint.route("/favourites/change_favourite/<game_id>")
@login_required
def change_favourite(game_id: str):
    user_name = None
    user_name = session["User_name"]
    try:
        # check that recived value is integer
        game_id = int(game_id)
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
    return redirect(url_for("favourites_bp.show_games"))
