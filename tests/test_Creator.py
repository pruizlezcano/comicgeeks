import pytest
from comicgeeks import Comic_Geeks

__author__ = "Pablo Ruiz"
__copyright__ = "Pablo Ruiz"
__license__ = "GPL-3.0-only"


def test_search_creator():
    """Search creator by name test"""
    client = Comic_Geeks()
    data = client.search_creator("Chip")
    assert len(data) > 1
    assert any(map(lambda x: x.name == "Chip Zdarsky", data))
    assert any(map(lambda x: x.creator_id == 6209, data))


def test_search_creator_error():
    """Search creator that doesn't exist test"""
    client = Comic_Geeks()
    data = client.search_creator("testing error")
    assert len(data) == 0


def test_get_creator_by_id():
    """Get creator by id test"""
    client = Comic_Geeks()
    data = client.creator_info(6209)
    assert len(data.characters) > 0
    assert len(data.series) > 0
    assert data.creator_id == 6209
    assert data.name == "Chip Zdarsky"
    assert data.description != ""
    assert data.image != "#"
    assert data.url == "/people/6209/chip-zdarsky"
    assert data.read is None
    assert data.owned is None
    assert data.issue_count >= 378
