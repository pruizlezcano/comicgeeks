import pytest
from comicgeeks import Comic_Geeks
from dotenv import dotenv_values
from pathlib import Path
from date import compare_timestamp

dotenv_path = Path(".devdata.env")
env = dotenv_values(dotenv_path=dotenv_path)
if "LCG_CI_SESSION" not in env:
    import os

    env = {
        "LCG_CI_SESSION": os.environ.get("LCG_CI_SESSION"),
        "LCG_USERNAME": os.environ.get("LCG_USERNAME"),
        "LCG_PASSWORD": os.environ.get("LCG_PASSWORD"),
    }

__author__ = "Pablo Ruiz"
__copyright__ = "Pablo Ruiz"
__license__ = "GPL-3.0-only"


def test_get_trade_paperback_by_id():
    """Get Trade Paperback by id test"""
    client = Comic_Geeks()
    data = client.issue_info(6828314).json()
    assert data["issue_id"] == 6828314
    assert len(data["characters"]) > 0
    cover = data["cover"]
    assert (
        cover["name"]
        == "Daredevil & Elektra by Chip Zdarsky Vol. 2: The Red Fist Saga Part Two TP"
        and cover["image"] != "#"
    )
    community = data["community"]
    assert (
        (
            community["pull"] >= 0
            if type(community["pull"]) is int
            else community["pull"] == "Unknown"
        )
        and (
            community["collect"] >= 0
            if type(community["collect"]) is int
            else community["collect"] == "Unknown"
        )
        and (
            community["readlist"] >= 0
            if type(community["readlist"]) is int
            else community["readlist"] == "Unknown"
        )
        and (
            community["wishlist"] >= 0
            if type(community["wishlist"]) is int
            else community["wishlist"] == "Unknown"
        )
        and (
            community["rating"] >= 0
            if type(community["rating"]) is int
            else community["rating"] == "Unknown"
        )
    )
    assert data["description"] != ""
    assert data["details"] == {
        "format": "trade paperback",
        "page_count": "112 pages",
        "isbn": "9781302932510",
        "distributor_sku": "apr230936",
    }
    assert data["name"] == "The Red Fist Saga Part Two"
    assert data["number"] == "2"
    assert len(data["person_credits"]) > 0
    assert data["price"] == 15.99
    assert data["publisher"] == "Marvel Comics"
    pagination = data["series_pagination"]
    assert all(
        map(
            lambda x: pagination[x] is not None,
            pagination.keys(),
        )
    )
    assert compare_timestamp(data["store_date"], 1690243200)
    assert (
        data["url"]
        == "/comic/6828314/daredevil-elektra-by-chip-zdarsky-vol-2-the-red-fist-saga-part-two-tp"
    )
    assert len(data["variant_covers"]) == 0
    user = data["user"]
    assert all(map(lambda x: user[x] is None, user.keys()))
    assert len(data["collects"]) > 0
