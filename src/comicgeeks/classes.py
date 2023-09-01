# Sorry, but due to circular imports, all of this must be in the same file
# Please, make a pull request if you know how to fix it

import datetime
import re
import requests
from bs4 import BeautifulSoup

from comicgeeks.extract import extract
from comicgeeks.utils import get_characters, get_series, randomword


class Issue:
    None


class Trade_Paperback:
    None


class Series:
    """ComicGeeks Series class"""

    def __init__(self, series_id: int, session: requests.Session):
        self._session = session
        self._series_id = series_id
        self._name = None
        self._publisher = None
        self._description = None
        self._start_year = None
        self._end_year = None
        self._issues = None
        self._issue_count = None
        self._trade_paperbacks = None
        self._trade_paperback_count = None
        self._url = None
        self._cover = None
        self._user = {"pull": None, "owned": None, "read": None}

    @property
    def user(self) -> dict:
        """Dictionary with user data

        Parameters:
            pull (bool) : Is the series in the pull list?,
            owned (str) : Is the issue in the collection?,
            read (str) : Is the issue in the read list?
        """
        if (
            self._user["pull"] is None
            or self._user["owned"] is None
            or self._user["read"] is None
        ) and self._session.authenticated:
            self._get_data()
        return self._user

    @property
    def series_id(self) -> int:
        """Series id"""
        if self._series_id is None:
            self._get_data()
        return self._series_id

    @property
    def issues(self) -> list[Issue]:
        """List of issues of the series"""
        if self._issues is None:
            self._get_data()
        return self._issues

    @property
    def trade_paperbacks(self) -> list[Trade_Paperback]:
        """List of trade paperbacks of the series"""
        if self._trade_paperbacks is None:
            self._get_data()
        return self._trade_paperbacks

    @property
    def description(self) -> str:
        """Series description"""
        if self._description is None:
            self._get_data()
        return self._description

    @property
    def name(self) -> str:
        """Series name"""
        if self._name is None:
            self._get_data()
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def url(self) -> str:
        """Series url"""
        if self._url is None:
            self._get_data()
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def start_year(self) -> int:
        """Year when the series started"""
        if self._start_year is None:
            self._get_data()
        return self._start_year

    @start_year.setter
    def start_year(self, value):
        self._start_year = value

    @property
    def end_year(self) -> int:
        """Year when the series ended"""
        if self._end_year is None:
            self._get_data()
        return self._end_year

    @end_year.setter
    def end_year(self, value):
        self._end_year = value

    @property
    def publisher(self) -> str:
        """Publisher name"""
        if self._publisher is None:
            self._get_data()
        return self._publisher

    @publisher.setter
    def publisher(self, value):
        self._publisher = value

    @property
    def cover(self) -> str:
        """Series cover url"""
        if self._cover is None:
            self._get_data()
        return self._cover

    @cover.setter
    def cover(self, value):
        self._cover = value

    @property
    def issue_count(self) -> int:
        """Number of issues"""
        if self._issue_count is None:
            self._get_data()
        return self._issue_count

    @issue_count.setter
    def issue_count(self, value):
        self._issue_count = value

    @property
    def trade_paperback_count(self) -> int:
        """Number of trade paperbacks"""
        if self._trade_paperback_count is None:
            self._get_data()
        return self._trade_paperback_count

    @trade_paperback_count.setter
    def trade_paperback_count(self, value):
        self._trade_paperback_count = value

    def _get_data(self):
        """Get series info"""
        url = f"https://leagueofcomicgeeks.com/comic/get_comics?&list=search&view=thumbs&format[]=1&series_id={self._series_id}&character=0&order=date-desc"
        r = self._session.get(url)
        r.raise_for_status()
        r = r.json()
        if r["count"] == 0:
            raise Exception("No series found")
        soup = BeautifulSoup(r["list"], features="lxml")
        header = BeautifulSoup(r["header"], features="lxml")
        statbar = BeautifulSoup(r["statbar"], features="lxml")
        time = header.find(class_="header-intro").text.split("·")[-1].split("-")
        begin = time[0]
        end = begin if len(time) == 1 else time[1]

        content = soup.find(id="comic-list-issues")
        issues = []
        for issue in content.find_all("li"):
            title = issue.find(class_="title").text.strip()
            name, number, volume = extract(title)
            issue_id = int(issue.find("a")["href"].split("/")[2])
            i = Issue(
                issue_id=issue_id,
                session=self._session,
            )

            i.name = title
            i.url = url
            i.store_date = issue.find(class_="date")["data-date"]
            i.price = (
                float(issue.find(class_="price").text.split("·")[1].strip()[1::])
                if issue.find(class_="price")
                else "Unknown"
            )
            i.publisher = r["series"]["publisher_name"]
            i.cover = issue.find("img")["data-src"]
            i.number = str(number) if number else ""
            comic_controller = issue.findAll(class_="comic-controller")
            i.user = {
                "pull": True if "active" in comic_controller[0]["class"] else False,
                "collect": True
                if len(comic_controller) >= 2
                and "active" in comic_controller[1]["class"]
                else False,
                "readlist": True
                if len(comic_controller) >= 3
                and "active" in comic_controller[2]["class"]
                else False,
                "wishlist": True
                if len(comic_controller) >= 4
                and "active" in comic_controller[3]["class"]
                else False,
                "rating": int(issue["data-rating"])
                if "data-rating" in issue
                else "Unknown",
            }
            issues.append(i)

        url = f"https://leagueofcomicgeeks.com/comic/get_comics?&list=search&view=thumbs&format[]=3&series_id={self._series_id}&character=0&order=date-desc"
        r = self._session.get(url)
        r.raise_for_status()
        r = r.json()
        trade_paperbacks = []
        if r["count"] > 0:
            soup = BeautifulSoup(r["list"], features="lxml")
            content = soup.find(id="comic-list-issues")

            for issue in content.find_all("li"):
                title = issue.find(class_="title").text.strip()
                number = re.findall(r"\d+", title)
                number = number[-1] if number else 1
                issue_id = int(issue.find("a")["href"].split("/")[2])
                i = Trade_Paperback(
                    issue_id=issue_id,
                    session=self._session,
                )

                i.name = title
                i.url = url
                i.store_date = issue.find(class_="date")["data-date"]
                i.price = (
                    float(issue.find(class_="price").text.split("·")[1].strip()[1::])
                    if issue.find(class_="price")
                    else "Unknown"
                )
                i.publisher = r["series"]["publisher_name"]
                i.cover = issue.find("img")["data-src"]
                i.number = str(number) if number else ""
                comic_controller = issue.findAll(class_="comic-controller")
                i.user = {
                    "pull": True if "active" in comic_controller[0]["class"] else False,
                    "collect": True
                    if len(comic_controller) >= 2
                    and "active" in comic_controller[1]["class"]
                    else False,
                    "readlist": True
                    if len(comic_controller) >= 3
                    and "active" in comic_controller[2]["class"]
                    else False,
                    "wishlist": True
                    if len(comic_controller) >= 4
                    and "active" in comic_controller[3]["class"]
                    else False,
                    "rating": int(issue["data-rating"])
                    if "data-rating" in issue
                    else "Unknown",
                }
                trade_paperbacks.append(i)

        self._name = r["series"]["title"]
        self._publisher = r["series"]["publisher_name"]
        self._description = BeautifulSoup(
            r["series"]["description"], features="lxml"
        ).text
        self._start_year = int(begin.strip()) if begin else 0
        self._end_year = int(end.strip()) if end and end.strip() != "Present" else 0
        self._issues = sorted(issues, key=lambda x: float(x.number))
        self._issue_count = len(issues)
        self._trade_paperbacks = sorted(trade_paperbacks, key=lambda x: float(x.number))
        self._trade_paperback_count = len(trade_paperbacks)
        self._url = header.find(class_="dropdown-item")["href"].split(
            "/submit-new-issue"
        )[0]
        self._cover = (
            header.find(class_="cover")["style"].split("'")[1]
            if header.find(class_="cover")
            else "#"
        )
        if self._session.authenticated:
            self._user["pull"] = True if statbar.find(class_="btn-remove") else False
            stats = statbar.findAll(class_="comic-score")
            if stats:
                self._user["owned"] = int(
                    stats[0]
                    .find(class_="text")
                    .text.strip()
                    .split("\n")[0]
                    .split(" ")[0]
                )
                self._user["read"] = (
                    int(
                        stats[1]
                        .find(class_="text")
                        .text.strip()
                        .split("\n")[0]
                        .split(" ")[0]
                    )
                    if len(stats) >= 2
                    else 0
                )
            else:
                self._user["owned"] = 0
                self._user["read"] = 0

    def pull(self) -> dict:
        """Pull series

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 1,
            "action": "subscribe",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def unsubscribe(self) -> dict:
        """Unsubscribe series

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 1,
            "action": "unsubscribe",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def pull_tp(self) -> dict:
        """Pull only trade paperback issues

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 1,
            "action": "subscribetp",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def pull_hc(self) -> dict:
        """Pull only hard cover issues

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 1,
            "action": "subscribehc",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def add_to_collection(self) -> dict:
        """Add series to collection

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 2,
            "action": "add",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def add_to_wishlist(self) -> dict:
        """Add series to wishlist

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 3,
            "action": "add",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def add_missing_to_wishlist(self) -> dict:
        """Add missing issues to wishlist

        Returns:
            dict: {"text": "", "type": "error|success"}
        """

        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 3,
            "action": "addnotowned",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def mark_read(self) -> dict:
        """Mark series as read

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 5,
            "action": "addall",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def mark_owned_read(self) -> dict:
        """Mark owned issues as read

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 5,
            "action": "addowned",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def remove_from_collection(self) -> dict:
        """Remove series from collection

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 2,
            "action": "remove",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def remove_from_wishlist(self) -> dict:
        """Remove series from wishlist

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 3,
            "action": "remove",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def remove_from_readlist(self) -> dict:
        """Mark series as unread

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_bulk"
        data = {
            "series_id": self._series_id,
            "list_id": 5,
            "action": "remove",
            "date": "",
            "date_type": "",
        }
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def json(self) -> dict:
        """Return data in json format"""
        return {
            "series_id": self._series_id,
            "name": self.name,
            "publisher": self.publisher,
            "description": self.description,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "issues": self.issues,
            "issue_count": self.issue_count,
            "trade_paperbacks": self.trade_paperbacks,
            "trade_paperback_count": self.trade_paperback_count,
            "url": self.url,
            "cover": self.cover,
            "user": self.user,
        }


class Issue:
    """ComicGeeks Issue class"""

    def __init__(self, issue_id: int, session: requests.Session):
        self._issue_id = issue_id
        self._session = session
        self._characters = None
        self._cover = None
        self._community = {
            "pull": None,
            "collect": None,
            "readlist": None,
            "wishlist": None,
            "rating": None,
        }
        self._user = {
            "pull": None,
            "collect": None,
            "readlist": None,
            "wishlist": None,
            "rating": None,
        }
        self._description = None
        self._details = None
        self._name = None
        self._number = None
        self._person_credits = None
        self._price = None
        self._publisher = None
        self._series_pagination = None
        self._store_date = None
        self._url = None
        self._variant_covers = None

    @property
    def characters(self) -> list:
        """List of characters that appear in this issue"""
        if self._characters is None:
            self._get_data()
        return self._characters

    @property
    def cover(self) -> dict:
        """Issue cover"""
        if self._cover is None:
            self._get_data()
        return self._cover

    @cover.setter
    def cover(self, value):
        self._cover = value

    @property
    def user(self) -> dict:
        """Dictionary with user data

        Parameters:
            pull (bool) : Is the issue in the pull list?,
            collect (bool) : Is the issue in the collection?,
            readlist (bool) : Is the issue in the read list?,
            wishlist (bool) : Is the issue in the wishlist?,
            rating (int) : User rating from 0 to 5

        """
        if (
            self._user["pull"] is None
            or self._user["collect"] is None
            or self._user["readlist"] is None
            or self._user["wishlist"] is None
            or self._user["rating"] is None
        ) and self._session.authenticated:
            self._get_data()
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def community(self) -> dict:
        """Dictionary with community data

        Parameters:
            pull (int|str) : Number of pulls or "Unknown" if the issue was already released,
            collect (int) : Number of users who have it,
            readlist (int) : Number of user who read it,
            wishlist (int) : Number of user who have it in their wishlist,
            rating (int) : Rating

        """
        if (
            self._community["pull"] is None
            or self._community["collect"] is None
            or self._community["readlist"] is None
            or self._community["wishlist"] is None
            or self._community["rating"] is None
        ):
            self._get_data()
        return self._community

    @community.setter
    def community(self, value):
        if "pull" in value:
            self._community["pull"] = value["pull"]
        if "collect" in value:
            self._community["collect"] = value["collect"]
        if "readlist" in value:
            self._community["readlist"] = value["readlist"]
        if "wishlist" in value:
            self._community["wishlist"] = value["wishlist"]
        if "rating" in value:
            self._community["rating"] = value["rating"]

    @property
    def description(self) -> str:
        """Issue description"""
        if self._description is None:
            self._get_data()
        return self._description

    @property
    def issue_id(self) -> int:
        """Issue id"""
        if self._issue_id is None:
            self._get_data()
        return self._issue_id

    @property
    def details(self) -> dict:
        """Issue details

        Parameters:
            format (str) : Issue format,
            page_count (str) : Number of pages,
            upc (str?) : UPC code,
            distributor_sku (str?) : SKU code,
        """
        if self._details is None:
            self._get_data()
        return self._details

    @property
    def name(self) -> str:
        """Issue name"""
        if self._name is None:
            self._get_data()
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def number(self) -> str:
        """Issue number"""
        if self._number is None:
            self._get_data()
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def person_credits(self) -> list:
        """List of people that create this issue"""
        if self._person_credits is None:
            self._get_data()
        return self._person_credits

    @property
    def price(self) -> float:
        """Issue price"""
        if self._price is None:
            self._get_data()
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def publisher(self) -> str:
        """Publisher name"""
        if self._publisher is None:
            self._get_data()
        return self._publisher

    @publisher.setter
    def publisher(self, value):
        self._publisher = value

    @property
    def series_pagination(self) -> dict:
        """Issue pagination

        Parameters:
            prev (Issue) : previous issue
            series (Series): series
            next (Issue): next issue
        """
        if self._series_pagination is None:
            self._get_data()
        return self._series_pagination

    @property
    def store_date(self) -> int:
        """Issue store date"""
        if self._store_date is None:
            self._get_data()
        return self._store_date

    @store_date.setter
    def store_date(self, value):
        self._store_date = value

    @property
    def url(self) -> str:
        """Issue url"""
        if self._url is None:
            self._get_data()
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def variant_covers(self) -> list:
        """List of variant covers"""
        if self._variant_covers is None:
            self._get_data()
        return self._variant_covers

    def _get_data(self):
        """Get series info"""
        url = f"https://leagueofcomicgeeks.com/comic/{self.issue_id}/{randomword(10)}"
        r = self._session.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, features="lxml")
        year, month, day = list(
            map(
                int,
                soup.find(class_="header-intro")
                .find_all("a")[1]["href"]
                .split("/")[3::],
            )
        )
        comic = soup.find(id="comic-details")
        details = comic.find(id="summary").find_all(class_="row")[-1]
        d = {}
        for detail in details.find_all(class_="details-addtl-block"):
            d[detail.find(class_="name").text.strip().lower().replace(" ", "_")] = (
                detail.find(class_="value").text.strip().lower()
            )
        price = d.pop("cover_price") if "cover_price" in d else "Unknown"
        price = float(price[1::]) if price != "Unknown" else price

        creators = comic.find(id="creators")
        person_credits = []
        if creators:
            creators = creators.find_all(class_="row")[1].find_all(class_="row")
            for creator in creators:
                creator_url = creator.find("a")["href"]
                creator_id = creator_url.split("/")[2]
                c = Creator(creator_id, self._session)
                c.url = creator_url
                c.name = creator.find(class_="name").text.strip()
                person_credits.append(
                    {
                        "role": creator.find(class_="role").text.strip().lower(),
                        "Creator": c,
                    }
                )

        characters = comic.find(id="characters")
        characters_credits = get_characters(characters, Character, self._session)

        covers = []
        cover = comic.find(class_="cover-art")
        covers.append(
            {
                "name": cover.find("img")["alt"],
                "image": cover.find("img")["src"],
            }
        )
        variant_covers = comic.find(class_="variant-cover-list")
        if variant_covers:
            for variant in variant_covers.find_all(class_="text-center"):
                img = variant.find("img")
                covers.append(
                    {
                        "name": img["alt"],
                        "url": variant.find("a")["href"],
                        "image": img["data-src"] if "data-src" in img else "#",
                    }
                )
        pagination = comic.find(class_="series-pagination")
        series_pagination = {
            "prev": Issue(
                pagination.find(class_="prev")["href"].split("/")[2],
                self._session,
            )
            if pagination.find(class_="prev")["href"] != "#"
            else None,
            "series": Series(
                pagination.find(class_="series")["href"].split("/")[3],
                self._session,
            )
            if pagination.find(class_="series")["href"] != "#"
            else None,
            "next": Issue(
                pagination.find(class_="next")["href"].split("/")[2],
                self._session,
            )
            if pagination.find(class_="next")["href"] != "#"
            else None,
        }
        counters = comic.findAll("span", class_="ml-1")
        counters_data = {}
        for counter in counters:
            text = counter.text.strip()
            if text != "":
                name = counter.parent()[0]["class"][0].split("-")[2]
                counters_data[name] = text

        counters_data["rating"] = soup.find(class_="percentage")
        if counters_data["rating"] is not None:
            counters_data["rating"] = counters_data["rating"].text.strip()

        title = soup.find("h1").text.strip()
        name, number, volume = extract(title)
        if type(self).__name__ == "Trade_Paperback":
            number = re.findall(r"\d+", title)[0]

        description: BeautifulSoup = comic.find(class_="listing-description")
        if comic.find(class_="story-title"):
            name: str = comic.find(class_="story-title").text.strip()
        else:
            name: str = title
        if type(self).__name__ == "Trade_Paperback":
            name = title.split(":")[1] if ":" in title else title
            name = name.replace("TP", "").strip()

        self._name = name.title()
        self._number = str(number) if number else ""
        self._publisher = soup.find(class_="header-intro").find("a").text.strip()
        self._store_date = int(datetime.datetime(year, month, day).timestamp())
        self._description = description.text.strip()
        self._details = d
        self._person_credits = person_credits
        self._characters = characters_credits
        self._cover = covers[0]
        self._variant_covers = covers[1:]
        self._series_pagination = series_pagination
        self._community["pull"] = (
            int(counters_data["pull"].replace(",", ""))
            if "pull" in counters_data
            else "Unknown"
        )
        self._community["collect"] = (
            int(counters_data["collect"].replace(",", ""))
            if "collect" in counters_data
            else "Unknown"
        )
        self._community["readlist"] = (
            int(counters_data["readlist"].replace(",", ""))
            if "readlist" in counters_data
            else "Unknown"
        )
        self._community["wishlist"] = (
            int(counters_data["wishlist"].replace(",", ""))
            if "wishlist" in counters_data
            else "Unknown"
        )
        self._community["rating"] = (
            int(counters_data["rating"].replace(",", ""))
            if "rating" in counters_data
            and counters_data["rating"] is not None
            and counters_data["rating"] != "TBD"
            else "Unknown"
        )
        self._price = price
        self._url = "/" + "/".join(r.url.split("/")[3:])

        if self._session.authenticated:
            counters = soup.findAll(class_="comic-controller")[1:]
            self._user["pull"] = True if "active" in counters[0]["class"] else False
            self._user["collect"] = (
                True
                if len(counters) >= 2 and "active" in counters[1]["class"]
                else False
            )
            self._user["readlist"] = (
                True
                if len(counters) >= 3 and "active" in counters[2]["class"]
                else False
            )
            self._user["wishlist"] = (
                True
                if len(counters) >= 4 and "active" in counters[3]["class"]
                else False
            )
            rate = soup.find(class_="rateit")
            self._user["rating"] = (
                int(rate["data-rateit-value"])
                if rate and "data-rateit-value" in rate
                else "Unknown"
            )
        if type(self).__name__ == "Trade_Paperback":
            collects = soup.find("section", id="collected-issues-list")
            if collects:
                collects = collects.find_all("li")
                self._collects = [
                    Issue(i.find("a")["href"].split("/")[2], self._session)
                    for i in collects
                ]
            else:
                self._collects = []

    def pull(self) -> dict:
        """Pull issue

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_move"
        data = {"comic_id": self.issue_id, "list_id": 1, "action_id": 1}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def unsubscribe(self) -> dict:
        """Unsubscribe issue

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_move"
        data = {"comic_id": self.issue_id, "list_id": 1, "action_id": 0}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def add_to_collection(self) -> dict:
        """Add issue to collection

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_move"
        data = {"comic_id": self.issue_id, "list_id": 2, "action_id": 1}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def remove_from_collection(self) -> dict:
        """Remove series from collection

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_move"
        data = {"comic_id": self.issue_id, "list_id": 2, "action_id": 0}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def mark_read(self) -> dict:
        """Mark issue as read

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_move"
        data = {"comic_id": self.issue_id, "list_id": 5, "action_id": 1}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def remove_from_readlist(self) -> dict:
        """Mark issue as unread

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_move"
        data = {"comic_id": self.issue_id, "list_id": 5, "action_id": 0}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def add_to_wishlist(self) -> dict:
        """Add series to wishlist

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_move"
        data = {"comic_id": self.issue_id, "list_id": 3, "action_id": 1}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def remove_from_wishlist(self) -> dict:
        """Remove series from wishlist

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/my_list_move"
        data = {"comic_id": self.issue_id, "list_id": 3, "action_id": 0}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def rate(self, score: int) -> dict:
        """Rate issue

        Args:
            score (int): number from 0 to 5

        Returns:
            dict: {"text": "", "type": "error|success"}
        """
        if not self._session.authenticated:
            return {"text": "No ci_session is given", "type": "error"}
        if score < 0 or score > 5:
            return {"text": "Score must be between 1 and 5", "type": "error"}
        url = "https://leagueofcomicgeeks.com/comic/post_rating"
        data = {"comic_id": self.issue_id, "score": score}
        r = self._session.post(url, data=data).json()
        return {"text": r["text"], "type": r["type"]}

    def json(self) -> dict:
        """Return data in json format"""
        r = {
            "issue_id": self.issue_id,
            "characters": self.characters,
            "cover": self.cover,
            "community": self.community,
            "description": self.description,
            "details": self.details,
            "name": self.name,
            "number": self.number,
            "person_credits": self.person_credits,
            "price": self.price,
            "publisher": self.publisher,
            "series_pagination": self.series_pagination,
            "store_date": self.store_date,
            "url": self.url,
            "variant_covers": self.variant_covers,
            "user": self.user,
        }
        if type(self).__name__ == "Trade_Paperback":
            r["collects"] = self.collects
        return r


class Trade_Paperback(Issue):
    def __init__(self, issue_id: int, session: requests.Session):
        super().__init__(issue_id, session)
        self._collects = None

    @property
    def collects(self) -> list[Issue]:
        """List of issues collected in this trade paperback"""
        if self._collects is None:
            self._get_data()
        return self._collects


class Creator:
    """Creator class"""

    def __init__(self, creator_id: int, session: requests.Session):
        self._characters = None
        self._session = session
        self._series = None
        self._creator_id = creator_id
        self._description = None
        self._image = None
        self._name = None
        self._url = None
        self._read = None
        self._owned = None
        self._issue_count = None

    @property
    def issue_count(self) -> int:
        """Number of issues made by this creator"""
        if self._issue_count is None and self._session.authenticated:
            self._get_data()
        return self._issue_count

    @property
    def read(self) -> int:
        """Issues by this creator read"""
        if self._read is None and self._session.authenticated:
            self._get_data()
        return self._read

    @property
    def owned(self) -> int:
        """Issues by this creator owned"""
        if self._owned is None and self._session.authenticated:
            self._get_data()
        return self._owned

    @property
    def description(self) -> list:
        """Creator description"""
        if self._description is None:
            self._get_data()
        return self._description

    @property
    def characters(self) -> list:
        """Credited characters"""
        if self._characters is None:
            self._get_data()
        return self._characters

    @property
    def series(self) -> list:
        """Credited series"""
        if self._series is None:
            self._get_data()
        return self._series

    @property
    def creator_id(self) -> list:
        """Creator id"""
        if self._creator_id is None:
            self._get_data()
        return self._creator_id

    @property
    def image(self) -> list:
        """Creator image"""
        if self._image is None:
            self._get_data()
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def name(self) -> list:
        """Creator name"""
        if self._name is None:
            self._get_data()
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def url(self) -> list:
        """Creator url"""
        if self._url is None:
            self._get_data()
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def _get_data(self):
        url = (
            f"https://leagueofcomicgeeks.com/people/{self.creator_id}/{randomword(10)}"
        )
        r = self._session.get(url)
        r.raise_for_status()
        comics_url = f"{r.url}/comics"
        comics_r = self._session.get(comics_url)
        comics_r.raise_for_status()
        comics_soup = BeautifulSoup(comics_r.content, features="lxml")
        soup = BeautifulSoup(r.content, features="lxml")

        self._name = soup.find(class_="page-details").find("h1").text.strip()
        self._description = (
            soup.find(class_="series-summary").find("p").text
            if soup.find(class_="series-summary")
            else ""
        )

        avatar = soup.find(class_="avatar")
        self._image = avatar.find("img")["src"] if avatar is not None else "#"
        self._url = r.url.split(".com")[1]

        characters = soup.find(id="characters")
        self._characters = get_characters(characters, Character, self._session)
        comics = comics_soup.find(id="comic-list-block").find_all("li")
        self._series = get_series(comics, Series, self._session)
        stats = comics_soup.findAll(class_="comic-score")
        if stats:
            self._issue_count = int(
                stats[0].find(class_="text").text.strip().split("\n")[0].split(" ")[2]
            )
        else:
            self._issue_count = "Unknown"
        if self._session.authenticated:
            if stats:
                self._owned = int(
                    stats[0]
                    .find(class_="text")
                    .text.strip()
                    .split("\n")[0]
                    .split(" ")[0]
                )
                self._read = int(
                    stats[1]
                    .find(class_="text")
                    .text.strip()
                    .split("\n")[0]
                    .split(" ")[0]
                )
            else:
                self._owned = 0
                self._read = 0

    def json(self) -> dict:
        """Return data in json format"""
        return {
            "characters": self.characters,
            "series": self.series,
            "creator_id": self.creator_id,
            "description": self.description,
            "image": self.image,
            "name": self.name,
            "url": self.url,
            "read": self.read,
            "owned": self.owned,
            "issue_count": self.issue_count,
        }


class Character:
    """Character class"""

    def __init__(self, character_id: int, session: requests.Session):
        self._character_id = character_id
        self._session = session
        self._image = None
        self._creators = None
        self._description = None
        self._information = None
        self._also_known_as = None
        self._series = None
        self._universe = None
        self._publisher = None
        self._name = None
        self._real_name = None
        self._url = None
        self._read = None
        self._owned = None
        self._issue_count = None

    @property
    def read(self) -> int:
        """Issues with this character read"""
        if self._read is None and self._session.authenticated:
            self._get_data()
        return self._read

    @property
    def issue_count(self) -> int:
        """Issues with this character"""
        if self._issue_count is None and self._session.authenticated:
            self._get_data()
        return self._issue_count

    @property
    def owned(self) -> int:
        """Issues with this character owned"""
        if self._owned is None and self._session.authenticated:
            self._get_data()
        return self._owned

    @property
    def image(self) -> str:
        """Character image"""
        if self._image is None:
            self._get_data()
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def creators(self) -> list:
        """Character creators"""
        if self._creators is None:
            self._get_data()
        return self._creators

    @property
    def description(self) -> str:
        """Character description"""
        if self._description is None:
            self._get_data()
        return self._description

    @property
    def information(self) -> list:
        """Information about the character"""
        if self._information is None:
            self._get_data()
        return self._information

    @property
    def also_known_as(self) -> list:
        """Other character personalities"""
        if self._also_known_as is None:
            self._get_data()
        return self._also_known_as

    @property
    def series(self) -> list:
        """Series in which the character appears"""
        if self._series is None:
            self._get_data()
        return self._series

    @property
    def universe(self) -> str:
        """Character universe"""
        if self._universe is None:
            self._get_data()
        return self._universe

    @universe.setter
    def universe(self, value):
        self._universe = value.strip()

    @property
    def publisher(self) -> str:
        """Character publisher"""
        if self._publisher is None:
            self._get_data()
        return self._publisher

    @publisher.setter
    def publisher(self, value):
        self._publisher = value.strip()

    @property
    def name(self) -> str:
        """Character real name"""
        if self._name is None:
            self._get_data()
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def real_name(self) -> str:
        """Character real name"""
        if self._real_name is None:
            self._get_data()
        return self._real_name

    @real_name.setter
    def real_name(self, value):
        self._real_name = value

    @property
    def url(self) -> str:
        """Character url"""
        if self._url is None:
            self._get_data()
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def character_id(self) -> str:
        """Character id"""
        if self._character_id is None:
            self._get_data()
        return self._character_id

    def _get_data(self):
        url = f"https://leagueofcomicgeeks.com/character/{self.character_id}/{randomword(10)}"
        r = self._session.get(url)
        r.raise_for_status()
        comics_url = f"{r.url}/comics"
        comics_r = self._session.get(comics_url)
        comics_r.raise_for_status()
        comics_soup = BeautifulSoup(comics_r.content, features="lxml")
        soup = BeautifulSoup(r.content, features="lxml")

        name = soup.find("h1").text.strip()
        self._name = name
        details = soup.find(class_="header-intro").text.strip().split("·")
        if len(details) == 3:
            real_name, publisher, universe = details
        else:
            real_name = name
            publisher, universe = details
        self._real_name = real_name.strip()
        self._publisher = publisher.strip()
        self._universe = universe.strip()
        self._description = (
            soup.find(class_="series-summary").text.strip()
            if soup.find(class_="series-summary")
            else ""
        )

        lists = soup.find(class_="content-sidebar-wrapper").findAll("ul")
        creators = []
        if lists:
            for creator in lists[0].findAll("li"):
                a = creator.find("a")
                if "people" in a["href"]:
                    creator_id = a["href"].split("/")[2]
                    c = Creator(creator_id, self._session)
                    c.name = creator.find(class_="title").text.strip()
                    c.url = a["href"]
                    creators.append(c)
        self._creators = creators

        info = []
        if len(lists) > 1:
            for i in lists[1].findAll("li"):
                info.append(
                    {
                        "key": i.find(class_="m-0").text.strip().replace("\n", " "),
                        "value": i.find(class_="copy-medium").text.strip(),
                    }
                )
        self._information = info

        self._image = (
            soup.find(class_="content-sidebar-wrapper").find("img")["src"]
            if soup.find(class_="content-sidebar-wrapper").find("img")
            else "#"
        )
        self._url = soup.find(class_="content-sidebar-wrapper").find("a")["href"]

        aka = []
        if soup.find(id="personas"):
            for persona in soup.find(id="personas").findAll(class_="name"):
                href = persona.find("a")["href"]
                if "character" in href:
                    aka.append({"name": persona.text.strip(), "url": href})
        self._also_known_as = aka
        comics = comics_soup.find(id="comic-list-block").find_all("li")
        self._series = get_series(comics, Series, self._session)
        stats = comics_soup.findAll(class_="comic-score")
        if stats:
            self._issue_count = int(
                stats[0].find(class_="text").text.strip().split("\n")[0].split(" ")[2]
            )
        if self._session.authenticated:
            if stats:
                self._owned = int(
                    stats[0]
                    .find(class_="text")
                    .text.strip()
                    .split("\n")[0]
                    .split(" ")[0]
                )
                self._read = (
                    int(
                        stats[1]
                        .find(class_="text")
                        .text.strip()
                        .split("\n")[0]
                        .split(" ")[0]
                    )
                    if len(stats) >= 2
                    else 0
                )
            else:
                self._issue_count = "Unknown"
                self._owned = 0
                self._read = 0

    def json(self) -> dict:
        """Return data in json format"""
        return {
            "character_id": self.character_id,
            "image": self.image,
            "creators": self.creators,
            "description": self.description,
            "information": self.information,
            "also_known_as": self.also_known_as,
            "series": self.series,
            "universe": self.universe,
            "publisher": self.publisher,
            "name": self.name,
            "real_name": self.real_name,
            "url": self.url,
            "read": self.read,
            "owned": self.owned,
            "issue_count": self.issue_count,
        }
