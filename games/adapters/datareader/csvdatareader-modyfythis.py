import os
import csv
from ..domainmodel.model import *


class GameFileCSVReader:

    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres

    def read_csv_file(self):
        if not os.path.isfile(self.__filename):
            raise FileNotFoundError
        else:
            with open(self.__filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    #game obj
                    game = Game(int(row['AppID']), row['Name'])
                    game.price = float(row['Price'])
                    game.release_date = row['Release date']
                    game.description = row['About the game']
                    game.image_url = row['Header image']
                    game.website_url = row['Website']
                    #game.reviews = row

                    #publsher obj
                    publisher = Publisher(row['Publishers'])
                    self.dataset_of_publishers.add(publisher)
                    game.publisher = publisher

                    #genre objs
                    genres = row['Genres'].split(",")
                    for genre in genres:
                        genre_obj = Genre(genre)
                        self.__dataset_of_genres.add(genre_obj)
                        game.add_genre(genre_obj)

                    self.__dataset_of_games.append(game)


