from sqlalchemy import select, inspect

from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['favourite_game', 'game', 'game_genre', 'genre', 'publisher', 'review',
                                           'user']


def test_database_populate_select_all_favourite_games(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_favourite_games_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table favourite_game
        select_statement = select([metadata.tables[name_of_favourite_games_table]])
        result = connection.execute(select_statement)

        all_favourite_games = []
        for row in result:
            all_favourite_games.append((row['user'], row['game']))

        num_favourite_games = len(all_favourite_games)
        assert num_favourite_games == 0


def test_database_populate_select_all_games(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table game
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['id'], row['title']))

        num_games = len(all_games)
        assert num_games == 877

        assert all_games[42] == (269250, 'WORLD END ECONOMiCA episode.01')


def test_database_populate_select_game_genre(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_game_genre_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table game_genre
        select_statement = select([metadata.tables[name_of_game_genre_table]])
        result = connection.execute(select_statement)

        all_game_genre = []
        for row in result:
            all_game_genre.append((row['game_id'], row['genre_name']))

        assert all_game_genre[17] == (45750, 'Action')
        assert all_game_genre[18] == (45750, 'Adventure')


def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table genre
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append(row['genre_name'])

        num_genres = len(all_genres)
        assert num_genres == 24

        assert all_genres[18] == 'Game Development'


def test_database_populate_select_all_publishers(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table publisher
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['name'])

        num_publishers = len(all_publishers)
        assert num_publishers == 798


def test_database_populate_select_all_reviews(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table review
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['user_id'], row['game_id'], row['rating'], row['comment']))

        num_reviews = len(all_reviews)
        assert num_reviews == 0


def test_database_populate_select_all_users(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table user
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        num_users = len(all_users)
        assert num_users == 0
