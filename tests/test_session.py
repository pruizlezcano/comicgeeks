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
    data = client._validate_session()
    assert data == False


def test_invalid_session():
    """Invalid session provided test"""
    client = Comic_Geeks()
    data = client._validate_session("1234")
    assert data == False


def test_valid_session():
    """Valid session provided test"""
    client = Comic_Geeks()
    data = client._validate_session(env["LCG_CI_SESSION"])
    assert data == True


def test_login():
    """Login test"""
    client = Comic_Geeks()
    data = client.login(env["LCG_USERNAME"], env["LCG_PASSWORD"])
    assert data == True


def test_invalid_login():
    """Invalid login test"""
    client = Comic_Geeks()
    data = client.login("test", "test")
    assert data == False
