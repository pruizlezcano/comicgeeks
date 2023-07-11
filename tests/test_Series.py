import pytest
from comicgeeks import Comic_Geeks
from dotenv import dotenv_values
from pathlib import Path

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


def test_search_series():
    """Search series by name test"""
    client = Comic_Geeks()
    data = client.search_series("Beta Ray Bill")
    assert len(data) > 1
    assert any(map(lambda x: x.name == "Beta Ray Bill", data))
    assert any(map(lambda x: x.series_id == 150065, data))


def test_search_series_error():
    """Search series that doesn't exist test"""
    client = Comic_Geeks()
    data = client.search_series("testing error")
    assert len(data) == 0


def test_get_series_by_id():
    """Get series by id test"""
    # Also test .json() function
    client = Comic_Geeks()
    data = client.series_info(150065).json()
    assert data["series_id"] == 150065
    assert data["name"] == "Beta Ray Bill"
    assert data["publisher"] == "Marvel Comics"
    assert data["description"] != ""
    assert data["start_year"] == 2021
    assert data["end_year"] == 2021
    assert len(data["issues"]) == 5
    assert data["issue_count"] == 5
    assert len(data["trade_paperbacks"]) == 1
    assert data["trade_paperback_count"] == 1
    assert data["url"] == "/comics/series/150065/beta-ray-bill"
    assert data["cover"] != "#"
    user = data["user"]
    assert all(map(lambda x: user[x] is None, user.keys()))


def test_get_series_by_id_session():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    data = client.series_info(150065)
    assert any(map(lambda x: data.user[x] is not None, data.user.keys()))


def test_add_missing():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.add_missing_to_wishlist()
    assert data["type"] == "success"


def test_add_collection():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.add_to_collection()
    assert data["type"] == "success"


def test_add_wishlist():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.add_to_wishlist()
    assert data["type"] == "success"


def test_mark_owned():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.mark_owned_read()
    assert data["type"] == "success"


def test_mark_read():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.mark_read()
    assert data["type"] == "success"


def test_pull():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.pull()
    assert data["type"] == "success"


def test_pull_hc():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.pull_hc()
    assert data["type"] == "success"


def test_pull_tp():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.pull_tp()
    assert data["type"] == "success"


def test_remove_collection():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.remove_from_collection()
    assert data["type"] == "success"


def test_remove_readlist():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.remove_from_readlist()
    assert data["type"] == "success"


def test_remove_wishlist():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.remove_from_wishlist()
    assert data["type"] == "success"


def test_unsubscribe():
    client = Comic_Geeks(env["LCG_CI_SESSION"])
    series = client.series_info(148315)
    data = series.unsubscribe()
    assert data["type"] == "success"


def test_add_missing_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.add_missing_to_wishlist()
    assert data["type"] == "error"


def test_add_collection_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.add_to_collection()
    assert data["type"] == "error"


def test_add_wishlist_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.add_to_wishlist()
    assert data["type"] == "error"


def test_mark_owned_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.mark_owned_read()
    assert data["type"] == "error"


def test_mark_read_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.mark_read()
    assert data["type"] == "error"


def test_pull_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.pull()
    assert data["type"] == "error"


def test_pull_hc_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.pull_hc()
    assert data["type"] == "error"


def test_pull_tp_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.pull_tp()
    assert data["type"] == "error"


def test_remove_collection_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.remove_from_collection()
    assert data["type"] == "error"


def test_remove_readlist_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.remove_from_readlist()
    assert data["type"] == "error"


def test_remove_wishlist_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.remove_from_wishlist()
    assert data["type"] == "error"


def test_unsubscribe_error():
    client = Comic_Geeks()
    series = client.series_info(150065)
    data = series.unsubscribe()
    assert data["type"] == "error"
