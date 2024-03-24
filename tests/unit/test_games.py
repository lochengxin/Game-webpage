import pytest

from typing import List, Iterable
from games.domainmodel.model import *
import games.adapters.repository as repo
import games.games.services as services

def test_get_games(in_memory_repo):
    assert repr(services.get_games(in_memory_repo, 30, 1)) == """[{'game_id': 3010, 'title': 'Xpand Rally', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/3010/header.jpg?t=1639506578', 'price': 4.99}, {'game_id': 7940, 'title': 'Call of Duty® 4: Modern Warfare®', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118', 'price': 9.99}, {'game_id': 11370, 'title': 'Nikopol: Secrets of the Immortals', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/11370/header.jpg?t=1634670183', 'price': 4.99}, {'game_id': 12140, 'title': 'Max Payne', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/12140/header.jpg?t=1618852800', 'price': 3.49}, {'game_id': 12460, 'title': 'BC Kings', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/12460/header.jpg?t=1573744168', 'price': 4.99}, {'game_id': 12670, 'title': 'Mission Runway', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/12670/header.jpg?t=1591334894', 'price': 9.99}, {'game_id': 16130, 'title': 'Fish Tycoon', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/16130/header.jpg?t=1447351298', 'price': 9.99}, {'game_id': 20200, 'title': 'Galactic Bowling', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/20200/header.jpg?t=1640121033', 'price': 19.99}, {'game_id': 22670, 'title': 'Alien Breed 3: Descent', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/22670/header.jpg?t=1655730869', 'price': 9.99}, {'game_id': 34282, 'title': 'Shadow Dancer™', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/34282/header.jpg?t=1549028434', 'price': 0.99}, {'game_id': 38160, 'title': 'Farm Frenzy 3: American Pie', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/38160/header.jpg?t=1447352918', 'price': 9.99}, {'game_id': 40420, 'title': 'Tidalis', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/40420/header.jpg?t=1591802519', 'price': 4.99}, {'game_id': 40800, 'title': 'Super Meat Boy', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/40800/header.jpg?t=1638306971', 'price': 14.99}, {'game_id': 42500, 'title': 'DogFighter', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/42500/header.jpg?t=1447352631', 'price': 0.99}, {'game_id': 42920, 'title': "The Kings' Crusade", 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/42920/header.jpg?t=1447353607', 'price': 9.99}, {'game_id': 45750, 'title': 'Lost Planet® 2', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/45750/header.jpg?t=1636428326', 'price': 0.0}, {'game_id': 50990, 'title': 'Mystery Case Files: Ravenhearst®', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/50990/header.jpg?t=1629483295', 'price': 9.99}, {'game_id': 65600, 'title': 'Gothic 3: Forsaken Gods Enhanced Edition', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/65600/header.jpg?t=1568714077', 'price': 9.99}, {'game_id': 108200, 'title': 'Ticket to Ride', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/108200/header.jpg?t=1621516042', 'price': 9.99}, {'game_id': 109500, 'title': 'Fowl Space', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/109500/header.jpg?t=1447355433', 'price': 4.99}, {'game_id': 110600, 'title': 'Astro Tripper', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/110600/header.jpg?t=1447354543', 'price': 4.99}, {'game_id': 110630, 'title': 'Mutant Storm: Reloaded', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/110630/header.jpg?t=1447355365', 'price': 4.99}, {'game_id': 201010, 'title': 'Geneforge 5: Overthrow', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/201010/header.jpg?t=1564012574', 'price': 19.99}, {'game_id': 205690, 'title': '1000 Amps', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/205690/header.jpg?t=1478107545', 'price': 4.99}, {'game_id': 219830, 'title': "King Arthur's Gold", 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/219830/header.jpg?t=1637137786', 'price': 0.0}, {'game_id': 220900, 'title': 'Jack Lumber', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/220900/header.jpg?t=1513875024', 'price': 4.99}, {'game_id': 223750, 'title': 'DCS World Steam Edition', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/223750/header.jpg?t=1658421899', 'price': 0.0}, {'game_id': 226620, 'title': 'Desktop Dungeons', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/226620/header.jpg?t=1640643139', 'price': 14.99}, {'game_id': 226780, 'title': 'MUD Motocross World Championship', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/226780/header.jpg?t=1654679678', 'price': 9.99}, {'game_id': 227160, 'title': 'Kinetic Void', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/227160/header.jpg?t=1447357131', 'price': 19.99}]"""
    assert repr(services.get_games(in_memory_repo, 30, 30)) == "[{'game_id': 2022020, 'title': 'Hidden Desert War Top-Down 3D', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/2022020/header.jpg?t=1655464884', 'price': 9.99}, {'game_id': 2023330, 'title': 'Fright Night', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/2023330/header.jpg?t=1655917847', 'price': 2.99}, {'game_id': 2026860, 'title': 'Maria Blanchard Virtual Gallery', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/2026860/header.jpg?t=1656711572', 'price': 0.0}, {'game_id': 2050890, 'title': 'ZombWave', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/2050890/header.jpg?t=1657288683', 'price': 1.99}, {'game_id': 2058120, 'title': 'Worm Runner', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/2058120/header.jpg?t=1657701620', 'price': 0.99}, {'game_id': 2061060, 'title': 'The Marson Home', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/2061060/header.jpg?t=1658157152', 'price': 7.99}, {'game_id': 2073470, 'title': 'Kanjozoku Game レーサー', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/2073470/header.jpg?t=1658578826', 'price': 5.99}]"
    
def test_get_max_page_num():
    assert services.get_max_page_num(100, 10) == 10
    assert services.get_max_page_num(101, 10) == 11
    assert services.get_max_page_num(10, 10) == 1
    assert services.get_max_page_num(1, 10) == 1
    
    
    
def test_generate_page_list():
    assert services.generate_page_list(1, 10) == [1, 2, 3, 4]
    assert services.generate_page_list(1, 2) == [1, 2]
    assert services.generate_page_list(1, 1) == [1]
    assert services.generate_page_list(5, 20) == [2, 3, 4, 5, 6, 7, 8]
    assert services.generate_page_list(20, 20) == [17, 18, 19, 20]
    
def test_get_current_display():
    assert services.get_current_display(100, 10, 1) == (1, 10)
    assert services.get_current_display(10, 10, 1) == (1, 10)
    assert services.get_current_display(1, 10, 1) == (1, 1)
    assert services.get_current_display(100, 10, 3) == (21, 30)
    assert services.get_current_display(100, 20, 3) == (41, 60)
    assert services.get_current_display(9, 10, 1) == (1, 9)
    
def test_get_number_of_games(in_memory_repo): 
    assert services.get_number_of_games(in_memory_repo) == 877

def test_get_favourite_list(in_memory_repo):
    user = User("root","Test1234")
    in_memory_repo.add_user(user)
    assert len(services.get_favourite_list(in_memory_repo,"root")) == 0

def test_change_favourite(in_memory_repo):
    user = User("root","Test1234")
    in_memory_repo.add_user(user)
    assert services.change_favourite(in_memory_repo,12140,"root") == True
    assert len(services.get_favourite_list(in_memory_repo,"root")) == 1

    