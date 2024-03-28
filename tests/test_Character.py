from pathlib import Path

import pytest
from load_env import load_env

from comicgeeks import Comic_Geeks

env = load_env()

__author__ = "Pablo Ruiz"
__copyright__ = "Pablo Ruiz"
__license__ = "GPL-3.0-only"


def test_search_character():
    """Search character by name test"""
    client = Comic_Geeks()
    data = client.search_character("daredevil")
    assert len(data) > 1
    assert any(map(lambda x: x.name == "Daredevil", data))
    assert any(map(lambda x: x.real_name == "Elektra Natchios", data))
    assert any(map(lambda x: x.character_id == 11699, data))


def test_search_character_error():
    """Search character that doesn't exist test"""
    client = Comic_Geeks()
    data = client.search_character("testing error")
    assert len(data) == 0


def test_get_character_by_id():
    """Get character by id test"""
    client = Comic_Geeks()
    data = client.character_info(11699).json()
    assert len(data["creators"]) > 0
    assert data["description"] != ""
    assert len(data["series"]) > 0
    assert data["image"] != "#"
    assert data["universe"] == "Earth-616"
    assert data["publisher"] == "Marvel Comics"
    assert data["name"] == "Daredevil"
    assert data["real_name"] == "Elektra Natchios"
    assert data["url"] == "/character/11699/daredevil"
    assert data["issue_count"] >= 37
    assert len(data["also_known_as"]) == 0
    assert data["owned"] is None
    assert data["read"] is None
    assert len(data["information"]) > 0


def test_get_character_by_id_session():
    """Get character by id test"""
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    print(env)
    assert env["LCG_CI_SESSION"] is not None
    data = client.character_info(11699)
    assert data.owned is not None
    assert data.read is not None


## TODO: character without creator credits
## TODO: character without aka
