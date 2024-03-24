import csv
import os

from games.domainmodel.model import Genre, Game, Publisher


class GameFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()

    def read_csv_file(self):
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
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
                    
                    
                    # game_id = int(row["AppID"])
                    # title = row["Name"]
                    # game = Game(game_id, title)
                    # game.release_date = row["Release date"]
                    # game.price = float(row["Price"])
                    # game.description = row["About the game"]

                    # publisher = Publisher(row["Publishers"])
                    # self.__dataset_of_publishers.add(publisher)
                    # game.publisher = publisher

                    # genre_names = row["Genres"].split(",")
                    # for genre_name in genre_names:
                    #     genre = Genre(genre_name.strip())
                    #     self.__dataset_of_genres.add(genre)
                    #     game.add_genre(genre)

                    # self.__dataset_of_games.append(game)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres
