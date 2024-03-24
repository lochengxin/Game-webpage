from flask import Blueprint, render_template, request, redirect, url_for, session
from games.domainmodel.model import *
from games.authentication.authentication import login_required

import games.authentication.authentication as authentication
import games.adapters.repository as repo
import games.profile.services as profile_services
import games.utilities.services as utilities_services


profile_blueprint = Blueprint("profile_bp", __name__)


@profile_blueprint.route('/profile', methods=['GET'])
@login_required
def show_profile():
    authenticated = authentication.check_authenticated()
    # if not authenticated:
    #     return redirect(url_for('home_bp.home'))
    user_name = session["User_name"]

    profile = profile_services.get_profile(repo.repo_instance, user_name)
    genre_list = utilities_services.get_genre_list(repo.repo_instance)

    return render_template("profile.html", profile=profile, genres=genre_list, authenticated=authenticated)


@profile_blueprint.route('/profile/remove_favourite/<game_id>', methods=['GET'])
@login_required
def remove_favourite(game_id):
    # authenticated = authentication.check_authenticated()
    # if not authenticated:
    #    return redirect(url_for('home_bp.home'))
    user_name = session["User_name"]

    utilities_services.remove_favourite(repo.repo_instance, user_name, int(game_id))

    return redirect(url_for("profile_bp.show_profile"))
