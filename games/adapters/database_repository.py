from abc import ABC
from typing import List

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import *

from games.adapters.repository import AbstractRepository
#from games.adapters.utils import search_string
from games.domainmodel.model import *


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    # defult function 
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        self.__game_list: List[Game] = list()

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def commit_session(self):
        self._session_cm.commit()

    #implemented
    def add_game(self, game: Game):
        """ Add a game to the repository list of games. """
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()
    
    #implemented
    def get_number_of_games(self) -> int:
        """ Returns a number of games exist in the repository. """
        number_of_game = self._session_cm.session.query(Game).count()
        return number_of_game
    
    #implemented
    def get_game_list(self) -> List[Game]:
        """" Returns the list of games. """
        game = self._session_cm.session.query(Game).all()
        return game
    
    #implemented
    def get_range_of_game_list(self, start: int, end: int, order: str = "game_id") -> List[Game]:
        """" Returns the list of games. """
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
        """" Returns the list of games. """
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


    # game atritbutes
    
    def get_game_by_id(self, game_id: int) -> Game:
        """" get game by id. """
        game = self._session_cm.session.query(Game).filter(Game._Game__game_id == int(game_id)).one()
        return game
    
    #implemented
    def get_game_title(self, game_obj: Game) -> str:
        """" get title of game by id. """
        result = None
        if game_obj is not None:
            result = game_obj.title
        return result
    
    #implemented
    def get_game_price(self, game_obj: Game) -> float:
        """" get price of the game by id. """
        result = None
        if game_obj is not None:
            result = game_obj.price
        return result
    
    #implemented
    def get_geme_release_date(self, game_obj: Game) -> str:
        """" get release_date of the game by id. """
        result = None
        if game_obj is not None:
            result = game_obj.release_date
        return result
    
    def get_game_description(self, game_obj: Game) -> str:
        """" get description of the game by id. """
        result = None
        if game_obj is not None:
            result = game_obj.description
        return result
    
    #implemented
    def get_game_image_url(self, game_obj: Game) -> str:
        """" get image_url of the game by id. """
        raise NotImplementedError
    
    def get_game_website_url(self, game_obj: Game) -> str:
        """" get website_url of the game by id. """
        result = None
        if game_obj is not None:
            result = game_obj.website_url
        return result

    #mostly
    def get_game_publisher(self, game_obj: Game) -> Publisher:
        """" get auther of game by id. """
        result = None
        if game_obj is not None:
            result = game_obj.publisher
        return result
    
    #mostly
    def get_game_genres(self, game_obj: Game) -> List[Genre]:
        """" get list of genres of the game by id. """
        result = None
        if game_obj is not None:
            result = game_obj.genres
        return result
    
    def get_game_reviews(self, game_obj: Game) -> List[Review]:
        """" get list of reviews of the game by id. """
        # result = None
        # if game_obj is not None:
        #     result = game_obj.reviews
        # return result

        reviews = self._session_cm.session.query(Review).filter(Review._Review__game > game_obj).all()
        return reviews
    
    #get games by xxx 
    
    # def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:
    #     """" get list of game by publisher. """
    #     raise NotImplementedError
    
    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        """" get list of game by genre. """
        games = self._session_cm.session.query(Game).filter(Game._Game__genres.contains(genre)).all()
        self.__game_list = games
        return games
    
    # about Search Function
    
    def get_game_search_list(self) -> List[Game]:
        """" Returns the list of games. """
        return self.__game_list

    #implemented
    def get_number_of_search_games(self) -> int:
        """ Returns a number of games exist in the repository. """
        return len(self.__game_list)
    
    #implemented
    def get_range_of_search_game_list(self, start: int, end: int, order: str = "game_id") -> List[Game]:
        """" Returns the list of games. """
        if isinstance(start, int) and isinstance(end, int) and isinstance(order, str):
            gamelist = self.__game_list
            
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
    #implemented
    def add_user(self, user: User) -> None:
        """" Adds a User to the repository. """
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()
    
    #implemented
    def get_user(self, user_name: str) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user
    

    # about genres class
    #implemented
    def add_genre(self, genre: Genre):
        """ Add a genre to the repository list of genres. """
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    #implemented
    def get_number_of_genres(self) -> int:
        """ Returns a number of genres exist in the repository. """
        number_of_genres = self._session_cm.session.query(Genre).count()
        return number_of_genres
    
    #implemented
    def get_genre_list(self) -> List[Genre]:
        """" Returns the list of genres. """
        genre = self._session_cm.session.query(Genre).all()
        return genre
    
    
    # about Publisher class
    #mostly
    def add_publisher(self, publisher: Publisher):
        """ Add a publisher to the repository list of publishers. """
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    #mostly
    def get_number_of_publisher(self) -> int:
        """ Returns a number of publishers exist in the repository. """
        number_of_publisher = self._session_cm.session.query(Publisher).count()
        return number_of_publisher
    
    #mostly
    def get_publisher_list(self) -> List[Game]:
        """" Returns the list of publishers. """
        publisher = self._session_cm.session.query(Publisher).all()
        return publisher
        
    #mostly
    def get_games_by_genre_str(self, genre: str) -> List[Game]:
        if genre is None:
            self.__game_list = []
            return None
        else:
            # Return games matching title; return an empty list if there are no matches.
            games = []
            game = self._session_cm.session.execute('SELECT game_id FROM game_genre WHERE genre_name LIKE :genre', {'genre': '%'+genre+'%'}).fetchall()
            if game is not None:
                for i in game:
                    games.append(self.get_game_by_id(i[0]))
            self.__game_list = games
            return games
    
    #mostly
    def get_games_by_publisher_str(self, publisher: str) -> List[Game]:
        if publisher is None:
            self.__game_list = []
            return None
        else:
            # Return games matching title; return an empty list if there are no matches.
            games = []
            game = self._session_cm.session.execute('SELECT id FROM game WHERE publisher_name LIKE :publisher', {'publisher': '%'+publisher+'%'}).fetchall()
            if game is not None:
                for i in game:
                    games.append(self.get_game_by_id(i[0]))
            self.__game_list = games
            return games
        
    #mostly
    def get_games_by_title_str(self, title: str) -> List[Game]:
        if title is None:
            self.__game_list = []
            return None
        else:
            # Return games matching title; return an empty list if there are no matches.
            games = self._session_cm.session.query(Game).filter(Game._Game__game_title.contains(title)).all()
            self.__game_list = games
            return games


     # about Review class
    def add_review(self, review: Review) -> None:
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()