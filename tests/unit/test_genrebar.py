import pytest

from typing import List, Iterable
from games.domainmodel.model import *
import games.adapters.repository as repo
import games.genre_bases.services as services



def test_repo_num_of_search_genre(in_memory_repo):
    genre = Genre("Action")
    in_memory_repo.get_games_by_genre(genre)
    assert in_memory_repo.get_number_of_search_games() == 380

def test_repo_get_max_page_num(in_memory_repo):
    assert services.get_max_page_num(380,30) == 13

def test_repo_generate_page_list(in_memory_repo):
    assert services.generate_page_list(1,13) == [1,2,3,4]

def test_repo_get_current_display(in_memory_repo):
    assert services.get_current_display(380,30,1) == (1,30)

def test_repo_get_genre_list(in_memory_repo):
    assert len(services.get_genre_list(in_memory_repo)) == 24

def test_repo_get_games(in_memory_repo):
    genre = Genre("Action")
    in_memory_repo.get_games_by_genre(genre)
    assert len(services.get_games(in_memory_repo,30,1,"")) == 30

def test_get_favourite_list(in_memory_repo):
    user = User("root","Test1234")
    in_memory_repo.add_user(user)
    assert len(services.get_favourite_list(in_memory_repo,"root")) == 0

def test_change_favourite(in_memory_repo):
    user = User("root","Test1234")
    in_memory_repo.add_user(user)
    assert services.change_favourite(in_memory_repo,12140,"root") == True
    assert len(services.get_favourite_list(in_memory_repo,"root")) == 1
    