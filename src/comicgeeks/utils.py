import random
import string
from typing import Union

import requests
from bs4 import NavigableString, Tag


def get_characters(
    content: Union[Tag, NavigableString, None], Character, session: requests.Session
):
    characters_credits = []
    if content is not None:
        characters = content.find_all(class_="row")[1].find_all(class_="row")
        for character in characters:
            url = character.find("a")["href"]
            character_id = int(url.split("/")[2])
            c = Character(character_id, session)
            c.name = character.find(class_="name").text.strip()
            c.url = url
            real_name = character.find(class_="real-name")
            if real_name:
                c.real_name = real_name.text.strip()
            universe = character.find(class_="universe")
            if universe:
                c.universe = universe.text.strip()
            characters_credits.append(c)
    return characters_credits


def get_creators(
    content: Union[Tag, NavigableString, None], Creator, session: requests.Session
):
    creators_credits = []
    if content is not None:
        content = content.find_all(class_="row")[1].find_all(class_="row")
        for creator in content:
            creator_url = creator.find("a")["href"]
            creator_id = creator_url.split("/")[2]
            c = Creator(creator_id, session)
            c.url = creator_url
            c.name = creator.find(class_="name").text.strip()
            creators_credits.append(
                {
                    "role": creator.find(class_="role").text.strip().lower(),
                    "Creator": c,
                }
            )
    return creators_credits


def get_series(content, Series, session: requests.Session):
    data = []
    for comic in content:
        a = comic.find("a")
        series = comic.find(class_="series")
        series_id = int(a["data-id"])
        s = Series(series_id, session)
        s.name = comic.find(class_="title").text.strip()
        s.url = a["href"]
        s.start_year = series["data-begin"]
        s.end_year = series["data-end"]
        s.publisher = comic.find(class_="publisher").text.strip()
        s.cover = comic.find("img")["data-src"]
        s.issue_count = comic.find(class_="count-issues").text.strip()
        data.append(s)
    return data


def is_trade_paperback(issue_id: int):
    url = f"https://leagueofcomicgeeks.com/comic/{issue_id}/{randomword(10)}"
    r = requests.get(url)
    return r.url[-3:] == "-tp"


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))
