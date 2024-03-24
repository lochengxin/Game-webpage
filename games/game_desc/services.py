from typing import List, Iterable
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import *

class NonExistentGameException(Exception):
    pass


class UnknownPageException(Exception):
    pass


def get_game(repo: AbstractRepository, game_id: int):
    if not isinstance(game_id, int):
        raise TypeError
    
    game_obj = repo.get_game_by_id(game_id)

    # Check the review numbers first to avoid ZeroDivisionError, then add to the dictionary
    if (len(game_obj.reviews) > 0):
        average_rating = int(round(sum(review.rating for review in game_obj.reviews) / len(game_obj.reviews), 1))
    else:
        average_rating = 0

    game = {
        "title": game_obj.title,
        "image_url": game_obj.image_url,
        "release_date": game_obj.release_date,
        "price": game_obj.price,
        "publisher_name": game_obj.publisher.publisher_name,
        # "rating": game_obj.reviews.rating,
        "website_url": game_obj.website_url,
        "genres": [genre.genre_name for genre in game_obj.genres],
        "description": game_obj.description,
        "game_reviews": game_obj.reviews,
        "num_game_reviews": len(game_obj.reviews),
        "game_reviews_average_rating": average_rating,
        "game_id": game_id

    }
    return game
    
def get_genre_list(repo: AbstractRepository) -> list:
    
    return repo.get_genre_list()


def get_user_review(repo: AbstractRepository, game_id: int) -> list:
    reviews = []
    game = repo.get_game_by_id(game_id)
    game_reviews: List[Review] =  game.reviews
    # print(game_reviews)
    for review in game_reviews:
        #add detail of reivew to dict and append to list of review 
        reviews.append({
            "user_name": review.user.username,
            "rating": review.rating,
            "comment": review.comment
        })
    return reviews

def change_favourite(repo: AbstractRepository, game_id: int, user_name: str) -> None:
    game = repo.get_game_by_id(int(game_id))
    user = repo.get_user(user_name)
    if (game not in user.favourite_games):
        user.add_favourite_game(game)
    else:
        user.remove_favourite_game(game)
    repo.commit_session()
    return True

def get_favourite_list(repo: AbstractRepository, game_id: int, user_name: str):
    favourite_list = False
    user = repo.get_user(user_name)
    game = repo.get_game_by_id(int(game_id))
    for i in user.favourite_games:
        if (i == game):
            favourite_list = True
            break
    return favourite_list

def review(repo: AbstractRepository, game_id: int, rate: int, comment: str, user_name:str) -> None:
    
    game = repo.get_game_by_id(game_id)
    user = repo.get_user(user_name)

    if not isinstance(game, Game) or not isinstance(user,User):
        raise TypeError
    else:
        #create new review object 
        review = Review(user,game,rate,comment)

        #add review object to game
        
        game.add_review(review)
        
        #add review object to user
        user.add_review(review)
        
        #add review to database
        repo.add_review(review)
        
        return True