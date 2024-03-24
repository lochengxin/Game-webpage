import pytest

from games.domainmodel.model import *
import games.profile.services as services


def test_profile_get_profile(in_memory_repo):
    user = User("kingsley", "1701Hanayo")
    in_memory_repo.add_user(user)

    dict_origin = services.get_profile(in_memory_repo, user.username)
    assert dict_origin["username"] == "kingsley"
    assert dict_origin["user_reviews"] == []
    assert dict_origin["user_favourite"] == []
    assert dict_origin["user_reviews_num"] == "0"
    assert dict_origin["user_favourite_num"] == "0"

    user.add_favourite_game(in_memory_repo.get_game_by_id(1002510))
    user.add_favourite_game(in_memory_repo.get_game_by_id(7940))
    user.add_review(Review(user, in_memory_repo.get_game_by_id(12140), 5, "Good game!"))

    dict_new = services.get_profile(in_memory_repo, user.username)
    assert dict_new["username"] == "kingsley"
    assert dict_new["user_reviews"] == [Review(user, in_memory_repo.get_game_by_id(12140), 5, "Good game!")]
    assert dict_new["user_favourite"] == [in_memory_repo.get_game_by_id(1002510), in_memory_repo.get_game_by_id(7940)]
    assert dict_new["user_reviews_num"] == "1"
    assert dict_new["user_favourite_num"] == "2"

def test_profile_remove_favourite(in_memory_repo):
    user = User("kingsley", "1701Hanayo")
    in_memory_repo.add_user(user)

    user.add_favourite_game(in_memory_repo.get_game_by_id(1002510))
    user.add_favourite_game(in_memory_repo.get_game_by_id(7940))

    services.remove_favourite(in_memory_repo, user.username, 7940)

    assert user.favourite_games == [in_memory_repo.get_game_by_id(1002510)]