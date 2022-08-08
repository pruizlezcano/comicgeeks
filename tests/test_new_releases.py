import pytest
from comicgeeks import Comic_Geeks
from datetime import datetime

__author__ = "Pablo Ruiz"
__copyright__ = "Pablo Ruiz"
__license__ = "GPL-3.0-only"


def test_new_releases():
    """New releases test"""
    client = Comic_Geeks()
    data = client.new_releases()
    assert len(data) > 0


def test_empty_new_releases():
    """Empty new releases test"""
    client = Comic_Geeks()
    data = client.new_releases(datetime(1111, 1, 1))
    assert len(data) == 0
