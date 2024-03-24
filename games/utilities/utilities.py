
# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication
import games.authentication.services as services

# ---------------------------------------

import games.utilities.services as services
utilities_blueprint  = Blueprint("utilities_bp", __name__)


# for check user already logedin or not
