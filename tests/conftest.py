import pytest

from games import create_app
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository
from pathlib import Path

TEST_DATA_PATH = Path(__file__).parent.parent / "games" / 'adapters' / 'data'


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, user_name='kingsley', password='1701Hanayo'):
        return self.__client.post(
            '/register',
            data={'user_name': user_name, 'password': password}
        )

    def login(self, user_name='kingsley', password='1701Hanayo'):
        return self.__client.post(
            '/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
