import pytest
from comicgeeks import Comic_Geeks
from dotenv import dotenv_values
from pathlib import Path

dotenv_path = Path(".devdata.env")
env = dotenv_values(dotenv_path=dotenv_path)

__author__ = "Pablo Ruiz"
__copyright__ = "Pablo Ruiz"
__license__ = "GPL-3.0-only"


def test_empty_session():
    """Session not provided test"""
    client = Comic_Geeks()
    data = client._check_session()
    assert data == ""


def test_invalid_session():
    """Invalid session provided test"""
    client = Comic_Geeks()
    data = client._check_session("1234")
    assert data == ""


def test_valid_session():
    """Valid session provided test"""
    client = Comic_Geeks()
    data = client._check_session(env["CI_SESSION"])
    assert data != ""
