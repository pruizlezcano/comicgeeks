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


def test_get_issue_by_id():
    """Get issue by id test"""
    # Also test .json() function
    client = Comic_Geeks()
    data = client.issue_info(3616996).json()
    assert data["issue_id"] == 3616996
    assert len(data["characters"]) > 0
    cover = data["cover"]
    assert cover["name"] == "Daredevil #8" and cover["image"] != "#"
    community = data["community"]
    assert (
        (
            community["pull"] >= 1
            if type(community["pull"]) is int
            else community["pull"] == "Unknown"
        )
        and (
            community["collect"] >= 1
            if type(community["collect"]) is int
            else community["collect"] == "Unknown"
        )
        and (
            community["readlist"] >= 1
            if type(community["readlist"]) is int
            else community["readlist"] == "Unknown"
        )
        and (
            community["wishlist"] >= 1
            if type(community["wishlist"]) is int
            else community["wishlist"] == "Unknown"
        )
        and (
            community["rating"] >= 1
            if type(community["rating"]) is int
            else community["rating"] == "Unknown"
        )
    )
    assert data["description"] != ""
    assert data["details"] == {
        "format": "comic",
        "page_count": "28 pages",
        "cover_date": "sep 2019",
        "upc": "75960609142300811",
        "distributor_sku": "may190864",
    }
    assert data["name"] == "No Devils, Only God, Part 3"
    assert data["number"] == "8"
    assert len(data["person_credits"]) > 0
    assert data["price"] == 3.99
    assert data["publisher"] == "Marvel Comics"
    pagination = data["series_pagination"]
    assert all(
        map(
            lambda x: pagination[x] is not None,
            pagination.keys(),
        )
    )
    assert compare_timestamp(data["store_date"], 1563321600)
    assert data["url"] == "/comic/3616996/daredevil-8"
    assert len(data["variant_covers"]) >= 2
    user = data["user"]
    assert all(map(lambda x: user[x] is None, user.keys()))


def test_get_issue_by_id_session():
    """Get issue by id test"""
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    data = client.issue_info(3616996)
    assert any(map(lambda x: data.user[x] is not None, data.user.keys()))


def test_get_issue_without_characters():
    """Get issue without characters credits test"""
    client = Comic_Geeks()
    data = client.issue_info(3943557)
    assert len(data.characters) == 0


def test_get_issue_without_variant_covers():
    """Get issue without variant covers test"""
    client = Comic_Geeks()
    data = client.issue_info(7757146)
    assert len(data.variant_covers) == 0


## TODO: issue without creator credits


def test_add_to_collection_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.add_to_collection()
    assert data["type"] == "error"


def test_add_to_wishlist_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.add_to_wishlist()
    assert data["type"] == "error"


def test_mark_read_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.mark_read()
    assert data["type"] == "error"


def test_pull_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.pull()
    assert data["type"] == "error"


def test_rate_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.rate(4)
    assert data["type"] == "error"


def test_remove_collection_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.remove_from_collection()
    assert data["type"] == "error"


def test_remove_readlist_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.remove_from_readlist()
    assert data["type"] == "error"


def test_remove_wishlist_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.remove_from_wishlist()
    assert data["type"] == "error"


def test_unsubscribe_error():
    client = Comic_Geeks()
    issue = client.issue_info(7757146)
    data = issue.unsubscribe()
    assert data["type"] == "error"


def test_add_to_collection():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.add_to_collection()
    assert data["type"] == "success"


def test_add_to_wishlist():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.add_to_wishlist()
    assert data["type"] == "success"


def test_mark_read():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.mark_read()
    assert data["type"] == "success"


def test_pull():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.pull()
    assert data["type"] == "success"


def test_rate():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.rate(0)
    assert data["type"] == "success"


def test_rate_invalid_error():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.rate(20)
    assert data["type"] == "error"


def test_remove_collection():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.remove_from_collection()
    assert data["type"] == "success"


def test_remove_readlist():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.remove_from_readlist()
    assert data["type"] == "success"


def test_remove_wishlist():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.remove_from_wishlist()
    assert data["type"] == "success"


def test_unsubscribe():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    issue = client.issue_info(7757146)
    data = issue.unsubscribe()
    assert data["type"] == "success"
