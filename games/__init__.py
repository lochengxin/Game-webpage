"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template, request

#for test 
from games.domainmodel.model import *

import games.adapters.repository as repo
from games.adapters.repository_populate import populate
from games.adapters.memory_repository import MemoryRepository
from games.adapters.orm import metadata, map_model_to_tables

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from games.adapters.database_repository import SqlAlchemyRepository
#from games.adapters.repository_populate import populate
from games.adapters.orm import metadata, map_model_to_tables


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    
    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'
    
    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
    
    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        # fill the repository from the provided CSV file

        populate(data_path, repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            populate(data_path, repo.repo_instance)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()


    with app.app_context():
        # Register the home blueprint to the app instance.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        # Register the game_desc blueprint to the app instance.
        from .game_desc import game_desc
        app.register_blueprint(game_desc.game_desc_blueprint)
        
        # Register the games blueprint to the app instance.
        from .games import games
        app.register_blueprint(games.games_blueprint)

        # Register the search blueprint to the app instance.
        from .search import search
        app.register_blueprint(search.search_blueprint)

        # Register the genre_bases blueprint to the app instance.
        from .genre_bases import genre_bases
        app.register_blueprint(genre_bases.genre_bases_blueprint)
        
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        # Register the profile blueprint to the app instance.
        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)

        # Register the profile blueprint to the app instance.
        from .favourites import favourites
        app.register_blueprint(favourites.favourites_blueprint)


    return app
