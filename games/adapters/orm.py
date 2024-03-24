from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, Float, 
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from games.domainmodel import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

# create table 
user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

genre_table = Table(
    'genre', metadata,
    Column('genre_name', String(255), primary_key=True, nullable=False)
)

publisher_table = Table(
    'publisher', metadata,
    Column('name', String(255), primary_key=True)
)

game_table = Table(
    'game', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('price', Float, nullable=False),
    Column('release_date', String(255)),
    Column('description', String(255)),
    Column('image', String(255)),
    Column('website', String(255)),
    Column('publisher_name', ForeignKey('publisher.name'))
)

review_table = Table(
    'review', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('user.id'), nullable=False),
    Column('game_id', ForeignKey('game.id'), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('comment', String(255), nullable=False)
)

favourite_table = Table(
    'favourite_game', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', ForeignKey('user.id'), nullable=False),
    Column('game', ForeignKey('game.id'), nullable=False)
)


# game genre table
game_genre_table = Table(
    'game_genre', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('game.id')),
    Column('genre_name', ForeignKey('genre.genre_name'))
)

# map model
def map_model_to_tables():
    mapper(model.User, user_table, properties={
        '_User__username': user_table.c.user_name,
        '_User__password': user_table.c.password,
        # many to many                        
        '_User__favourite_games': relationship(model.Game, secondary=favourite_table) ,
        # review 
        '_User__reviews': relationship(model.Review, back_populates="_Review__user")
    })

    mapper(model.Genre, genre_table, properties={
        '_Genre__genre_name': genre_table.c.genre_name
    })

    mapper(model.Publisher, publisher_table, properties={
        '_Publisher__publisher_name': publisher_table.c.name
    })
    
    mapper(model.Game, game_table, properties={
        '_Game__game_id': game_table.c.id,
        '_Game__game_title': game_table.c.title,
        '_Game__price': game_table.c.price,
        '_Game__release_date': game_table.c.release_date,
        '_Game__description': game_table.c.description,
        '_Game__image_url': game_table.c.image,
        '_Game__website_url': game_table.c.website,
        # publisher
        # one to many
        '_Game__publisher': relationship(model.Publisher),
        # many to many
        '_Game__genres': relationship(model.Genre, secondary=game_genre_table),
        # review
        # one to many        
        '_Game__reviews': relationship(model.Review, back_populates="_Review__game")

    })

    mapper(model.Review, review_table, properties={
        # one to many
        '_Review__user': relationship(model.User, back_populates="_User__reviews"),
        # one to many                                      
        '_Review__game': relationship(model.Game, back_populates="_Game__reviews"),
        '_Review__rating': review_table.c.rating,
        '_Review__comment': review_table.c.comment 
    })