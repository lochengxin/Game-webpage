from bisect import insort_left
from typing import List
import os
from pathlib import Path
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import *
from games.adapters.datareader.csvdatareader import GameFileCSVReader

# errors
class GameNotFoundException(Exception):
    def __init__(self, message=None):
        pass

# reop class
class MemoryRepository(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self.__games: List[Game] = list()
        self.__genres: List[Genre] = list()
        self.__publishers: List[Publisher] = list()
        self.__users: List[User] = list()
        #self.__reviews: List[Review] = list()
        
        self.__game_list: List[Game] = list()
    
    # about Game class 
    def add_game(self, game: Game):
        if isinstance(game, Game):
            # When inserting the game, keep the game list sorted alphabetically by the id.
            # Games will be sorted by game due to __lt__ method of the Game class.
            insort_left(self.__games, game)
            
    def get_game_list(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)
    
    def get_game_by_id(self, game_id: int) -> Game:
        if isinstance(game_id, int):
            for game in self.__games:
                if game.game_id == game_id:
                    # return str(game_id)
                    return game
            raise GameNotFoundException
        else:
            raise TypeError
    
    def get_range_of_game_list(self, start: int, end: int, order: str = "game_id") -> List[Game]:
        if isinstance(start, int) and isinstance(end, int) and isinstance(order, str):
            gamelist = self.get_game_list()
            
            if order == "game_id":
                gamelist.sort(key= lambda game: game.game_id)
            elif order == "title":
                gamelist.sort(key=lambda game: game.title)
            elif order == "publisher":
                gamelist.sort(key=lambda game: game.publisher.publisher_name)
            elif order == "release_date":
                gamelist.sort(key=lambda game: game.release_date)
            elif order == "price":
                gamelist.sort(key=lambda game: game.price)
            else: 
                gamelist.sort(key= lambda game: game.game_id)
            
            
            gamelist = gamelist[start:end]
            return gamelist
            
        else:
            raise TypeError
        
    def get_range_of_favourite_game_list(self, user: User, start: int, end: int, order: str = "game_id") -> List[Game]:
        if isinstance(start, int) and isinstance(end, int) and isinstance(order, str):
            gamelist = user.favourite_games
            
            if order == "game_id":
                gamelist.sort(key= lambda game: game.game_id)
            elif order == "title":
                gamelist.sort(key=lambda game: game.title)
            elif order == "publisher":
                gamelist.sort(key=lambda game: game.publisher.publisher_name)
            elif order == "release_date":
                gamelist.sort(key=lambda game: game.release_date)
            elif order == "price":
                gamelist.sort(key=lambda game: game.price)
            else: 
                gamelist.sort(key= lambda game: game.game_id)
            
            
            gamelist = gamelist[start:end]
            return gamelist
            
        else:
            raise TypeError
        
    
    def get_game_title(self, game_obj: Game) -> str:
        return game_obj.title
        
    def get_game_price(self, game_obj: Game) -> float:
        return game_obj.price
    
    def get_geme_release_date(self, game_obj: Game) -> str:
        return game_obj.release_date
    
    def get_game_description(self, game_obj: Game) -> str:
        return game_obj.description
    
    def get_game_image_url(self, game_obj: Game) -> str:
        return game_obj.image_url
    
    def get_game_website_url(self, game_obj: Game) -> str:
        return game_obj.website_url
    
    def get_game_publisher(self, game_obj: Game) -> Publisher:
        return game_obj.publisher
    
    def get_game_genres(self, game_obj: Game) -> List[Genre]:
        return game_obj.genres
        
    def get_game_reviews(self, game_obj: Game) -> List[Review]:
        return game_obj.reviews
    
    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        if isinstance(genre, Genre):
            game_list: List[Game] = list()
            
            # look for the games that have the genre from arg
            for game in self.__games:
                if genre in game.genres and genre not in game_list:
                    insort_left(game_list, game)
                    
            self.__game_list = game_list
            return self.__game_list
        
    # def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:
    #     if isinstance(publisher, Publisher):
    #         game_list: List[Game] = list()
    #
    #         # look for games that have same publisher form arg
    #         for game in self.__games:
    #             if publisher == game.publisher:
    #                 insort_left(game_list, game)
    #
    #         self.__game_list = game_list
    #         return game_list
        
    def get_games_by_genre_str(self, genre: str) -> List[Game]:
        
            game_list: List[Game] = list()
            
            # look for the games that have the genre from arg
            for game in self.__games:
                for gen in game.genres:
                    if genre.lower() in gen.genre_name.lower():
                        insort_left(game_list, game)
                        break
                    
            self.__game_list = game_list
            return self.__game_list
    
    def get_games_by_publisher_str(self, publisher: str) -> List[Game]:
            game_list: List[Game] = list()
            
            # look for games that have same publisher form arg
            for game in self.__games:
                if publisher.lower() in game.publisher.publisher_name.lower():
                    insort_left(game_list, game)
            
            self.__game_list = game_list
            return game_list
        
    def get_games_by_title_str(self, title: str) -> List[Game]:
            game_list: List[Game] = list()
            
            # look for games that have same publisher form arg
            for game in self.__games:
                if title.lower() in game.title.lower():
                    insort_left(game_list, game)
            
            self.__game_list = game_list
            return game_list
        
     # about Search Function

    def get_game_search_list(self) -> List[Game]:
        return self.__game_list

    def get_number_of_search_games(self):
        return len(self.__game_list)
    
    def get_range_of_search_game_list(self, start: int, end: int, order: str = "game_id") -> List[Game]:
        if isinstance(start, int) and isinstance(end, int) and isinstance(order, str):
            gamelist = self.get_game_search_list()
            
            if order == "game_id":
                gamelist.sort(key= lambda game: game.game_id)
            elif order == "title":
                gamelist.sort(key=lambda game: game.title)
            elif order == "publisher":
                gamelist.sort(key=lambda game: game.publisher.publisher_name)
            elif order == "release_date":
                gamelist.sort(key=lambda game: game.release_date)
            elif order == "price":
                gamelist.sort(key=lambda game: game.price)
            else: 
                gamelist.sort(key= lambda game: game.game_id)
            
            gamelist = gamelist[start:end]
            return gamelist
            
        else:
            raise TypeError
        
        
    # about User class 
    def add_user(self, user: User) -> None:
        self.__users.append(user)

    def get_user(self, user_name: str) -> User:
        return next((user for user in self.__users if user.username == user_name), None)
            
    # about Genre class

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            insort_left(self.__genres, genre)
            
    def get_genre_list(self) -> List[Genre]:
        return self.__genres

    def get_number_of_genres(self) -> int:
        return len(self.__genres)
    
    
    # about Publisher class
    

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            insort_left(self.__publishers, publisher)

    def get_number_of_publisher(self) -> int:
        return len(self.__publishers)
    
    def get_publisher_list(self) -> List[Game]:
        return self.__publishers
    
    def commit_session(self):
        pass

    def add_review(self, review: Review) -> None:
        pass


    
# add all game data to the memory repo obj using datareader
def populate(data_path: Path, repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(data_path, "games.csv")
    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    games = reader.dataset_of_games
    genres = reader.dataset_of_genres
    publishers = reader.dataset_of_publishers
    # reviews = reader.dataset
    
    for publisher in publishers:
        repo.add_publisher(publisher)

    # Add games to the repo
    for game in games:
        repo.add_game(game)
        
    for genre in genres:
        repo.add_genre(genre)
        
        