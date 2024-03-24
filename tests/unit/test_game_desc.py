import pytest

from games.domainmodel.model import *
import games.game_desc.services as services


def test_game_desc_get_game(in_memory_repo):
    game_dict = services.get_game(in_memory_repo, 1002510)

    assert game_dict["title"] == "The Spell - A Kinetic Novel"
    assert game_dict["image_url"] == "https://cdn.akamai.steamstatic.com/steam/apps/1002510/header.jpg?t=1592930600"
    assert game_dict["release_date"] == "Jan 15, 2019"
    assert game_dict["price"] == 4.99
    assert game_dict["publisher_name"] == "Hangover Cat Purrroduction"
    assert game_dict["website_url"] == "https://www.hangovercatpurrroduction.com/"
    assert game_dict["genres"] == ["Casual", "Indie"]
    assert game_dict["description"] == ("Story After a tragic incident which took the lives of both her parents, "
                                        "Eloise is forced to live with a man claiming to be her uncle. Indifferent, "
                                        "weird, and expressionless, he’s everything that Eloise would normally define "
                                        "as ‘unreliable’. Yet, little by little, she finds herself opening up to this "
                                        "odd and mysterious character named Steve. She even comes to believe that "
                                        "maybe everything will be alright from now on. That is, until she found a "
                                        "weird note concerning her parents’ deaths next to the garbage bin. Features "
                                        "60k words story Original Soundtrack Kinetic novel")
    assert game_dict["game_reviews"] == []
    assert game_dict["num_game_reviews"] == 0
    assert game_dict["game_reviews_average_rating"] == 0


def test_game_desc_get_genre_list(in_memory_repo):
    assert services.get_genre_list(in_memory_repo) == in_memory_repo.get_genre_list()


# def test_game_desc_get_publisher_list(in_memory_repo):
    # assert services.get_publisher_list(in_memory_repo) == in_memory_repo.get_publisher_list()

def test_get_favourite_list(in_memory_repo):
    user = User("root","Test1234")
    in_memory_repo.add_user(user)
    assert services.get_favourite_list(in_memory_repo,12140,"root") == False

def test_get_game(in_memory_repo):
    assert services.get_game(in_memory_repo,12140)["game_id"] == 12140

def test_review(in_memory_repo):
    user = User("root","Test1234")
    in_memory_repo.add_user(user)
    assert services.review(in_memory_repo,12140,3,"shdkghskdjl","root") == True

def test_change_favourite(in_memory_repo):
    user = User("root","Test1234")
    in_memory_repo.add_user(user)
    assert services.change_favourite(in_memory_repo,12140,"root") == True

