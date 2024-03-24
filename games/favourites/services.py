from typing import List, Iterable
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

class NonExistentGameException(Exception):
    pass


class UnknownPageException(Exception):
    pass


def get_games(repo: AbstractRepository, games_per_page: int,  pagenum: int, user_name: str, order: str = ""):
    if not isinstance(games_per_page, int) or not isinstance(pagenum, int) or pagenum<1:
        raise UnknownPageException
    
    start_index = games_per_page*(pagenum-1)
    end_index = games_per_page*pagenum
    
    if end_index > get_number_of_games(repo,user_name) -1:
        end_index = get_number_of_games(repo,user_name)
         
    user = repo.get_user(user_name)
    

    # games = repo.get_game_list()[start_index: end_index]
    games = repo.get_range_of_favourite_game_list(user, start_index, end_index, order)
    game_dicts = []
    for game in games:
        game_dict = {
            "game_id": game.game_id,
            "title": game.title,
            "image_url": game.image_url,
            "price": game.price
        }
        game_dicts.append(game_dict)
    return game_dicts
  
def get_max_page_num(number_of_games: int, games_per_page: int) -> int:
    if isinstance(number_of_games, int) and isinstance(games_per_page, int):    
        # max page number is #of games/ game par page if divisible, if not +1 
        maxpage = number_of_games//games_per_page 
        if not number_of_games % games_per_page == 0:
            maxpage += 1
        return maxpage
    
    
def generate_page_list(current_page, max_page):
    page_list = []

    for n in range(-3, 4):
        new_page = current_page + n

        if 1 <= new_page <= max_page:
            page_list.append(new_page)

    return page_list

def get_current_display(num_of_games:int, games_per_page:int, current_page: int): #return what game is the page sohowing in sence of total number of games might be display
    if isinstance(num_of_games, int) and isinstance(games_per_page, int) and isinstance(current_page, int):
        start = games_per_page*(current_page-1) +1
        end = games_per_page*current_page
        
        if end > num_of_games:
            end = num_of_games

        return (start, end)
    
def change_favourite(repo: AbstractRepository, game_id: int, user_name: str) -> None:
    game = repo.get_game_by_id(int(game_id))
    user = repo.get_user(user_name)
    if (game not in user.favourite_games):
        user.add_favourite_game(game)
    else:
        user.remove_favourite_game(game)
    return None


def get_number_of_games(repo: AbstractRepository, user_name: str) -> int:
    user = repo.get_user(user_name)
    return len(user.favourite_games)

def get_genre_list(repo: AbstractRepository) -> list:
    return repo.get_genre_list()
