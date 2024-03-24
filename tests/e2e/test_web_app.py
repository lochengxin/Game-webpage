import pytest

from flask import session


# Test registering
def test_e2e_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/register',
        data={'user_name': 'kingsley', 'password': '1701Hanayo'}
    )
    assert response.headers['Location'] == '/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('kingsley', '1701Hanayo', b'This user name is already taken - please enter another'),
))
def test_e2e_register_with_invalid_input(client, auth, user_name, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    auth.register()  # Register a user first to test if the client tries registering with the same username.
    response = client.post(
        '/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


# Test logging in
def test_e2e_login(client, auth):
    auth.register()  # Register a user first to use this user to test login.
    # Check that we can retrieve the login page.
    status_code = client.get('/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == '/home'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['User_name'] == 'kingsley'


# Test accessing page that require login
def test_e2e_required_login(client):
    response = client.get('/profile')
    assert response.headers['Location'] == '/login'


# Test browsing games
def test_e2e_layout_page(client):
    # Check that we can retrieve the layout page.
    response = client.get('/')
    response_layout = client.get('/home')
    assert response.status_code == 200
    assert response_layout.status_code == 200

    # Check that the introduction is included on the page.
    assert b'Welcome to the CS235 Game Library!' in response.data
    assert b'Welcome to the CS235 Game Library!' in response_layout.data


def test_e2e_games_page_default(client):
    # Check that we can retrieve the games page.
    response = client.get('/games')
    assert response.status_code == 200

    # Check that the first 3 games we need are included on the page.
    assert b'Xpand Rally' in response.data
    assert b'Call of Duty' in response.data
    assert b'Nikopol: Secrets of the Immortals' in response.data


def test_e2e_games_page_with_page_num(client):
    # Check that we can retrieve the games page with page num.
    response_page_1 = client.get('/games?page=1')
    response_page_2 = client.get('/games?page=2')
    assert response_page_1.status_code == 200
    assert response_page_2.status_code == 200

    # Check that the first 3 games we need are included on the page.
    assert b'Xpand Rally' in response_page_1.data
    assert b'Call of Duty' in response_page_1.data
    assert b'Nikopol: Secrets of the Immortals' in response_page_1.data

    assert b'Deadfall Adventures' in response_page_2.data
    assert b'Hexodius' in response_page_2.data
    assert b'Expeditions: Conquistador' in response_page_2.data


def test_e2e_games_page_with_order(client):
    # Check that we can retrieve the games page with order.
    response_price = client.get('/games?page=2&order=price')
    response_game_id = client.get('/games?page=2&order=game_id')
    response_title = client.get('/games?page=2&order=title')
    response_publisher = client.get('/games?page=2&order=publisher')
    response_release_date = client.get('/games?page=2&order=release_date')
    assert response_price.status_code == 200
    assert response_game_id.status_code == 200
    assert response_title.status_code == 200
    assert response_publisher.status_code == 200
    assert response_release_date.status_code == 200

    # Check that the first 3 games we need are included on the page.
    assert b'MagiCats Builder (Crazy Dreamz)' in response_price.data
    assert b'Lumberjack VR' in response_price.data
    assert b'Google Spotlight Stories: Special Delivery' in response_price.data

    assert b'Deadfall Adventures' in response_game_id.data
    assert b'Hexodius' in response_game_id.data
    assert b'Expeditions: Conquistador' in response_game_id.data

    assert b'Alien Planet' in response_title.data
    assert b'Aliens vs. Ghosts' in response_title.data
    assert b'Alone In The Mars' in response_title.data

    assert b'Into the Pyramid' in response_publisher.data
    assert b'Gripper' in response_publisher.data
    assert b'SC2KRender' in response_publisher.data

    assert b'VELONE' in response_release_date.data
    assert b'Gem Tower Defense 2' in response_release_date.data
    assert b'Darza' in response_release_date.data


def test_e2e_game_desc(client):
    response = client.get('/gameDescription/1002510')
    assert response.status_code == 200
    assert b'The Spell - A Kinetic Novel' in response.data


def test_e2e_game_desc_not_found(client):
    response = client.get('/gameDescription/114514')
    assert response.status_code == 200
    assert b'game id: 114514 is not found.' in response.data


# Test adding/ removing games to the favourite list
def test_e2e_games_page_favourite(client, auth):
    # Check if we can use the button in the games page to add/ remove favourite.
    # Register and login a user.
    auth.register()
    auth.login()

    # Add favourite by the button in the games page.
    response_add = client.get('/game/change_favourite/1002510')
    assert response_add.status_code == 200
    response_add_check = client.get('/favourites')
    assert response_add_check.status_code == 200
    assert b'The Spell - A Kinetic Novel' in response_add_check.data

    # Remove favourite by the button in the games page.
    response_remove = client.get('/game/change_favourite/1002510')
    assert response_remove.status_code == 200
    response_remove_check = client.get('/favourites')
    assert response_remove_check.status_code == 200
    assert b'The Spell - A Kinetic Novel' not in response_remove_check.data


def test_e2e_game_desc_page_favourite(client, auth):
    # Check if we can use the button in the game_desc page to add/ remove favourite.
    # Register and login a user.
    auth.register()
    auth.login()

    # Add favourite by the button in the game_desc page.
    response_add = client.get('/gameDescription/change_favourite/1002510')
    assert response_add.status_code == 302
    response_add_check = client.get('/favourites')
    assert response_add_check.status_code == 200
    assert b'The Spell - A Kinetic Novel' in response_add_check.data

    # Remove favourite by the button in the game_desc page.
    response_remove = client.get('/gameDescription/change_favourite/1002510')
    assert response_remove.status_code == 302
    response_remove_check = client.get('/favourites')
    assert response_remove_check.status_code == 200
    assert b'The Spell - A Kinetic Novel' not in response_remove_check.data


def test_e2e_favourite_page_remove_favourite(client, auth):
    # Check if we can use the button in the favourite page to remove favourite.
    # Register and login a user.
    auth.register()
    auth.login()

    # Add favourite by the button in the game_desc page.
    response_add = client.get('/gameDescription/change_favourite/1002510')
    assert response_add.status_code == 302
    response_add_check = client.get('/favourites')
    assert response_add_check.status_code == 200
    assert b'The Spell - A Kinetic Novel' in response_add_check.data

    # Remove favourite by the button in the favourite page.
    response_remove = client.get('/favourites/change_favourite/1002510')
    assert response_remove.status_code == 302
    response_remove_check = client.get('/favourites')
    assert response_remove_check.status_code == 200
    assert b'The Spell - A Kinetic Novel' not in response_remove_check.data


# Test Comment and profile page
def test_e2e_comment_and_profile(client, auth):
    # Register and login a user.
    auth.register()
    auth.login()

    # Write a comment and check if the game_desc page shows the comment.
    response_comment = client.get('/review/1002510/5/Good%20game!')
    response_game_desc = client.get('/gameDescription/1002510')
    assert response_comment.status_code == 302
    assert response_game_desc.status_code == 200
    assert b'Good game!' in response_game_desc.data

    # Check if the profile page shows the comment.
    response_profile = client.get('/profile')
    assert response_profile.status_code == 200
    assert b'Good game!' in response_profile.data


# Test logging out
def test_e2e_logout(client, auth):
    # Register and login a user.
    auth.register()
    auth.login()

    auth.logout()
    response = client.get('/home')
    assert b'kingsley' not in response.data
