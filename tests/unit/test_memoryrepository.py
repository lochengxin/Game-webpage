import pytest

from games.domainmodel.model import *


# Test repository can add a game object
def test_repo_can_add_a_game(in_memory_repo):
    # Set the new game, and add it into the repo
    game = Game(897220, 'Summer Pockets')
    in_memory_repo.add_game(game)

    # Check if the repo includes the new game
    assert in_memory_repo.get_game_by_id(897220) is game


# Test repository can retrieve a game object
def test_repo_can_retrieve_a_game(in_memory_repo):
    # Get the game we need
    game = in_memory_repo.get_game_by_id(1002510)

    # Check if this is the game we want
    assert game == Game(1002510, "The Spell - A Kinetic Novel")


# Test repository retrieves correct number of game objects
def test_repo_retrieves_correct_num_of_game(in_memory_repo):
    # Get the total num of games in the repo
    game_num = in_memory_repo.get_number_of_games()

    # Check if the total num is matched
    assert game_num == 877


# Test the number of unique genres in the dataset
def test_repo_num_of_unique_genre(in_memory_repo):
    # Get the total num of genres in the repo
    genre_num = in_memory_repo.get_number_of_genres()

    # Check if the total num is matched
    assert genre_num == 24


# Test repository adds a new genre, and the count of genres increases by 1
def test_repo_add_new_genre_and_increase_count(in_memory_repo):
    # Get the origin num of genres
    genre_num = in_memory_repo.get_number_of_genres()

    # Set the new genre, and add it into the repo
    genre = Genre("Visual Novel")
    in_memory_repo.add_genre(genre)

    # Check if the new genre is inside the all genre list
    assert genre in in_memory_repo.get_genre_list()

    # Check if the num of genres has been increased by 1
    assert genre_num + 1 == in_memory_repo.get_number_of_genres()


# Test repository search games by title
def test_repo_search_game_by_title(in_memory_repo):
    # Search all games with a title that includes "dragon"
    search_result = in_memory_repo.get_games_by_title_str("dragon")

    # Check if the title of every game from the search result includes "dragon", case-insensitive
    for game in search_result:
        assert "dragon" in game.title.lower()


# Test repository search games by publisher
# def test_repo_search_game_by_publisher(in_memory_repo):
#     # Set the publisher
#     publisher = Publisher("Boogygames Studios")
#
#     # Search all games from the publisher
#     search_result = in_memory_repo.get_games_by_publisher(publisher)
#
#     # Check if the num of search results is matched
#     assert len(search_result) == 2
#
#     # Check the publisher of every game from the search results
#     for game in search_result:
#         assert game.publisher == publisher


# Test repository search games by genre
def test_repo_search_game_by_genre(in_memory_repo):
    # Set the genre
    genre = Genre("Indie")

    # Search all games with this genre
    search_result = in_memory_repo.get_games_by_genre(genre)

    # Check if the num of search results is matched
    assert len(search_result) == 649

    # Check if every game from the search results includes this genre
    for game in search_result:
        assert genre in game.genres


# Test repository search games by genre name
def test_repo_search_game_by_genre_name(in_memory_repo):
    # Set the potential genre, for checking
    genre = Genre("Racing")

    # Search all games with this genre, by name
    search_result = in_memory_repo.get_games_by_genre_str("Racing")

    # Check if the num of search results is matched
    assert len(search_result) == 31

    # Check if every game from the search results includes the potential genre
    for game in search_result:
        assert genre in game.genres


# Test repository search games by genre
def test_repo_get_range_of_favourite_game_list(in_memory_repo):
    user = User("root","Test1234")

    assert len(in_memory_repo.get_range_of_favourite_game_list(user,0,9)) == 0 

def test_get_user(in_memory_repo):
    user = User("root","Test1234")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user("root") == user

