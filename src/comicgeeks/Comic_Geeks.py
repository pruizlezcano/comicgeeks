from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup

from comicgeeks.classes import Character, Creator, Issue, Series, Trade_Paperback
from comicgeeks.utils import get_series, is_trade_paperback


class Comic_Geeks:
    """League of Comic Geeks client

    Attributes:
        ci_session (str): Cookie ci_session of League of Comic Geeks
    """

    def __init__(self, ci_session: str = None) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
            }
        )
        self._session.authenticated = False
        self._session.authenticated = False
        if self._validate_session(ci_session):
            self._session.authenticated = True

    def login(self, username: str, password: str) -> bool:
        """Login to League of Comic Geeks

        Args:
            username (str): Username
            password (str): Password

        Returns:
            str: ci_session cookie
        """
        url = "https://leagueofcomicgeeks.com/login"
        r = self._session.post(url, data={"username": username, "password": password})
        r.raise_for_status()
        ci_session = self._validate_session(r.cookies.get("ci_session"))
        if ci_session:
            self._session.authenticated = True
            return True
        else:
            self._session.authenticated = False
            return False

    def _validate_session(self, ci_session: str = None) -> bool:
        """Check if session is valid.
        Make a request to the main page and if is redirected to the dashboard, the session is valid.
        """
        if ci_session is None or ci_session == "":
            return False
        r = self._session.get(
            "https://leagueofcomicgeeks.com/", cookies={"ci_session": ci_session}
        )
        r.raise_for_status()
        if "dashboard" in r.url:
            return True
        self._session.cookies.clear()  # Clear invalid ci_session
        return False

    def search_series(self, query: str) -> list[Series]:
        """Search series by name

        Args:
            query (str): Series name

        Returns:
            list (Series): List of series
        """
        query = query.strip().lower().replace(" ", "+")
        url = f"https://leagueofcomicgeeks.com/comic/get_comics?&list=search&list_option=series&view=thumbs&title={query}&order=alpha-asc&format[]=1&format[]=6"
        r = self._session.get(url)
        r.raise_for_status()
        r = r.json()
        if r["count"] == 0:
            return []

        soup = BeautifulSoup(r["list"], features="lxml")
        content = soup.find(id="comic-list-block")
        comics = content.find_all("li")
        data = get_series(comics, Series, self._session)
        return data

    def search_creator(self, query: str) -> list[Creator]:
        """Search series by name

        Args:
            query (str): Series name

        Returns:
            list (Series): List of series
        """
        query = query.strip().lower().replace(" ", "+")
        url = f"https://leagueofcomicgeeks.com/search/creators?keyword={query}"
        r = self._session.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, features="lxml")
        content = soup.find(class_="comic-series-thumb-list")
        if content is None:
            return []
        data = []
        for item in content.findAll("li"):
            creator_id = int(item.find("a")["href"].split("/")[2])
            creator = Creator(creator_id, self._session)
            creator.name = item.find(class_="title").text.strip()
            creator.url = item.find("a")["href"]
            if item.find("img"):
                creator.image = item.find("img")["src"]
            data.append(creator)
        return data

    def search_character(self, query: str) -> list[Character]:
        query = query.strip().lower().replace(" ", "+")
        url = f"https://leagueofcomicgeeks.com/search/characters?keyword={query}"
        r = self._session.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, features="lxml")
        content = soup.find(class_="character-thumb-list")
        if content is None:
            return []
        data = []
        for item in content.findAll("li"):
            character_id = int(item.find("a")["href"].split("/")[2])
            character = Character(character_id, self._session)
            character.name = item.find(class_="title").text.strip()
            character.url = item.find("a")["href"]
            character.real_name = (
                item.find(class_="publisher").text.strip()
                if item.find(class_="publisher")
                else ""
            )
            if item.find(class_="series"):
                character.publisher, character.universe = item.find(
                    class_="series"
                ).text.split("·")
            if item.find("img"):
                character.image = item.find("img")["data-src"]
            data.append(character)
        return data

    def new_releases(self, date: datetime = "now") -> list[Issue]:
        """Get this week new releases

        Args:
            date (datetime): Date to get new releases

        Returns:
            list (Issue): List of issues
        """
        if date == "now":
            date = datetime.now()
        date = f"{date.month}/{date.day}/{date.year}"

        url = f"https://leagueofcomicgeeks.com/comic/get_comics?list=releases&view=thumbs&format[]=1%2C6&date_type=week&date={date}&order=pulls"
        r = self._session.get(url).json()
        if r["count"] == 0:
            return []

        soup = BeautifulSoup(r["list"], features="lxml")
        content = soup.find(id="comic-list-block")
        comics = content.find_all("li")
        data = []
        for comic in comics:
            a = comic.find("a")
            price = (
                float(comic.find(class_="price").text.split("·")[1].strip()[1::])
                if comic.find(class_="price")
                else "Unknown"
            )
            pulls = comic["data-pulls"]
            rating = comic["data-community"]
            name = comic.find(class_="title").text.strip()
            issue_id = int(a["href"].split("/")[2])
            url = a["href"]
            store_date = comic.find(class_="date")["data-date"]
            publisher = comic.find(class_="publisher").text.strip()
            cover = comic.find("img")["data-src"]
            community = {"rating": rating, "pull": pulls}

            issue = Issue(
                issue_id=issue_id,
                session=self._session,
            )

            issue.name = name
            issue.url = url
            issue.store_date = store_date
            issue.price = price
            issue.publisher = publisher
            issue.cover = cover
            issue.community = community
            data.append(issue)
        return data

    def series_info(self, series_id: int) -> Series:
        """Get series info by id

        Args:
            series_id (int): series id

        Returns:
            Series: Series class
        """
        return Series(series_id, self._session)

    def issue_info(self, issue_id: int) -> Union[Issue, Trade_Paperback]:
        """Get issue info by id

        Args:
            issue_id (int): issue id

        Returns:
            Issue | Trade_Paperback: Issue object
        """
        if is_trade_paperback(issue_id):
            return Trade_Paperback(issue_id, self._session)
        return Issue(issue_id, self._session)

    def creator_info(self, creator_id: int) -> Creator:
        """Get creator info by id

        Args:
            creator_id (int): creator id

        Returns:
            Creator: Creator object
        """
        return Creator(creator_id, self._session)

    def character_info(self, character_id: int) -> Character:
        """Get character info by id

        Args:
            character_id (int): character id

        Returns:
            Character: Character object
        """
        return Character(character_id, self._session)
