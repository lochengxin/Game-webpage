# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication
import games.utilities.services as utilities


# ---------------------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps
import games.authentication.services as services

authentication_blueprint  = Blueprint("authentication_bp", __name__)

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None
    authenticated = check_authenticated()
    
    #data for sidebar 
    genres_list = utilities.get_genre_list(repo.repo_instance)
    
    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('authentication_bp.login')) # only when no error occur
        
        except services.NameNotUniqueException:
            user_name_not_unique = "This user name is already taken - please enter another"
            
    return render_template(
        "authentication/credentials.html", 
        title="Register",
        genres=genres_list,
        user_name_error_message=user_name_not_unique,
        form=form,
        handler_url=url_for('authentication_bp.register'),
        authenticated=authenticated
    )



@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None
    authenticated = check_authenticated()
    
    #data for sidebar 
    genres_list = utilities.get_genre_list(repo.repo_instance)

    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)
            
            
            # authenticate user
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)
            
            session.clear()
            session['User_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))
        
        except services.UnknownUserException:
            user_name_not_recognised = "User name not recognised - please supply another"
        except services.AuthenticationException:
            password_does_not_match_user_name = "Password does not match supplied user name - please check and try again"
    
    
    return render_template(
        "authentication/credentials.html",
        title = "Login",
        genres=genres_list,
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form,
        authenticated=authenticated
    )
    
@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def check_authenticated() -> bool: # return true if already login 
    return "User_name" in session   

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'User_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view

class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField(
        'Username', 
        validators=[
            DataRequired(message='Your user name is required'),
            Length(min=3, message='Your user name is too short')
        ],
        render_kw={
            "placeholder": "User name is not case sensitive",
            "class": "text-input"
        }
    )
    
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message='Your password is required'),
            PasswordValid()
        ],
        render_kw={
            "placeholder": "Password",
            "class": "text-input", 
            "size": "40"
        }
    )
    
    submit = SubmitField('Register', render_kw={"class": "form_submit_button"})
    
class LoginForm(FlaskForm):
    user_name = StringField(
        'Username', 
        validators=[DataRequired(message='Your user name is required')],
        render_kw={
            "placeholder": "User name is not case sensitive",
            "class": "text-input"
        }
    )
    
    password = PasswordField(
        'Password', 
        validators=[DataRequired(message='Your password is required')],
        render_kw={
            "placeholder": "Password",
            "class": "text-input", 
            "size": "40"
        }
    )
    
    submit = SubmitField('Login', render_kw={"class": "form_submit_button"})
        
        