import os
from pathlib import Path
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import *
from games.adapters.datareader.csvdatareader import GameFileCSVReader


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

