import requests
from bs4 import BeautifulSoup

from .classes import Character, Creator, Issue, Series
from .utils import get_series

_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
}


class Comic_Geeks:
    """League of Comic Geeks client

    Attributes:
        ci_session (str): Cookie ci_session of League of Comic Geeks
    """

    def __init__(self, ci_session: str = None) -> None:
        self._ci_session: str = self._check_session(ci_session)

    def _check_session(self, ci_session: str) -> bool:
        """Check if session is valid.
        Make a request to the main page and if is redirected to the dashboard, the session is valid.
        """
        if ci_session is None:
            return ""
        s = requests.Session()
        s.cookies.update({"ci_session": ci_session})
        r = s.get("https://leagueofcomicgeeks.com/", headers=_headers)
        if "dashboard" in r.url:
            return ci_session
        return ""

    def search_series(self, query: str) -> list[Series]:
        """Search series by name

        Args:
            query (str): Series name

        Returns:
            list (Series): List of series
        """
        query = query.strip().lower().replace(" ", "+")
        url = f"https://leagueofcomicgeeks.com/comic/get_comics?&list=search&list_option=series&view=thumbs&title={query}&order=alpha-asc&format[]=1&format[]=6"
        r = requests.get(url, headers=_headers)
        r.raise_for_status()
        r = r.json()
        if r["count"] == 0:
            return []

        soup = BeautifulSoup(r["list"], features="lxml")
        content = soup.find(id="comic-list-block")
        comics = content.find_all("li")
        data = get_series(comics, Series, self._ci_session)
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
        r = requests.get(url, headers=_headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, features="lxml")
        content = soup.find(class_="comic-series-thumb-list")
        if content is None:
            return []
        data = []
        for item in content.findAll("li"):
            creator_id = int(item.find("a")["href"].split("/")[2])
            creator = Creator(creator_id, self._ci_session)
            creator.name = item.find(class_="title").text.strip()
            creator.url = item.find("a")["href"]
            if item.find("img"):
                creator.image = item.find("img")["src"]
            data.append(creator)
        return data

    def search_character(self, query: str) -> list[Character]:
        query = query.strip().lower().replace(" ", "+")
        url = f"https://leagueofcomicgeeks.com/search/characters?keyword={query}"
        r = requests.get(url, headers=_headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, features="lxml")
        content = soup.find(class_="character-thumb-list")
        if content is None:
            return []
        data = []
        for item in content.findAll("li"):
            character_id = int(item.find("a")["href"].split("/")[2])
            character = Character(character_id, self._ci_session)
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

    def new_releases(self) -> list[Issue]:
        """Get this week new releases

        Returns:
            list (Issue): List of issues
        """
        url = "https://leagueofcomicgeeks.com/comic/get_comics?list=releases&view=thumbs&format[]=1%2C6&date_type=week&date=now&order=pulls"
        r = requests.get(url, headers=_headers).json()
        if r["count"] == 0:
            return []

        soup = BeautifulSoup(r["list"], features="lxml")
        content = soup.find(id="comic-list-block")
        comics = content.find_all("li")
        data = []
        for comic in comics:
            a = comic.find("a")
            price = comic.find(class_="price")
            if price is not None:
                price = price.text.split("·")[1].strip()[1::]
                if "£" in price:
                    price = price[1::]
            else:
                price = 0
            pulls = comic["data-pulls"]
            rating = comic["data-community"]
            name = comic.find(class_="title").text.strip()
            issue_id = int(a["href"].split("/")[2])
            url = a["href"]
            store_date = comic.find(class_="date")["data-date"]
            price = float(price)
            publisher = comic.find(class_="publisher").text.strip()
            cover = comic.find("img")["data-src"]
            community = {"rating": rating, "pulls": pulls}

            issue = Issue(
                issue_id=issue_id,
                ci_session=self._ci_session,
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
        return Series(series_id, self._ci_session)

    def issue_info(self, issue_id: int) -> Issue:
        """Get issue info by id

        Args:
            issue_id (int): issue id

        Returns:
            Issue: Issue object
        """
        return Issue(issue_id, self._ci_session)

    def creator_info(self, creator_id: int) -> Creator:
        """Get creator info by id

        Args:
            creator_id (int): creator id

        Returns:
            Creator: Creator object
        """
        return Creator(creator_id, self._ci_session)

    def character_info(self, character_id: int) -> Character:
        """Get character info by id

        Args:
            character_id (int): character id

        Returns:
            Character: Character object
        """
        return Character(character_id, self._ci_session)
