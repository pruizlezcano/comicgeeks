# Getting started

## Installation

Install the package (or add it to your ``requirements.txt`` file):

```console
$ pip install comicgeeks
```

## Getting cookie session

In order to use some of the package functions, you will need to provide a valid cookie session.
To do that, follow this steps:

1. Login into [League of Comics Geeks ](https://leagueofcomicgeeks.com/)
2. Open you browser's dev tools and search for the `ci_session` cookie
3. Use the cookie value to create a session when calling the package class `Comic_Geeks(ci_session)`

## Usage

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks("mycisession")

# search series
client.search_series("daredevil")

# get new releases
client.new_releases()

# get info about an issue
client.issue_info(3616996)
```

Check the [examples](/examples) tab for more use cases.
