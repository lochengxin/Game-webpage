import pytest

from games.domainmodel.model import *
import games.authentication.services as services


def test_authentication_add_user(in_memory_repo):
    services.add_user("kingsley", "1701Hanayo", in_memory_repo)

    assert in_memory_repo.get_user("kingsley") != None


def test_authentication_get_user(in_memory_repo):
    user = User("kingsley", "1701Hanayo")
    in_memory_repo.add_user(user)
    dict = services.get_user("kingsley", in_memory_repo)

    assert dict["user_name"] == 'kingsley'
    assert dict["password"] == '1701Hanayo'
