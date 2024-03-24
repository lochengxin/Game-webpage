from games.adapters.repository import AbstractRepository
from games.domainmodel.model import *


class NonExistentGameException(Exception):
    pass


class UnknownPageException(Exception):
    pass


def get_profile(repo: AbstractRepository, username: str):
    if not isinstance(username, str):
        raise TypeError

    user = repo.get_user(username)
    profile_dict = {
        "username": user.username,
        "user_reviews": user.reviews,
        "user_favourite": user.favourite_games,
        "user_reviews_num": str(len(user.reviews)),
        "user_favourite_num": str(len(user.favourite_games))
    }
    return profile_dict


def remove_favourite(repo: AbstractRepository, username: str, game_id: int):
    if not isinstance(username, str):
        raise TypeError

    if not isinstance(game_id, int):
        raise TypeError

    user = repo.get_user(username)
    game = repo.get_game_by_id(game_id)

    user.remove_favourite_game(game)

    return None
