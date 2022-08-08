[![PyPI](https://img.shields.io/pypi/v/comicgeeks?color=5593c8&logoColor=a7bfc1&style=for-the-badge)](https://pypi.org/project/comicgeeks/)
[![Coveralls](https://img.shields.io/coveralls/github/pruizlezcano/comicgeeks?style=for-the-badge)](https://coveralls.io/github/pruizlezcano/comicgeeks?branch=main)
[![forthebadge](https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg)](https://forthebadge.com)
# comicgeeks

> A python client for League of Comics Geeks.

* Search series, creators and characters by name
* Get series, issues, creators and characters information
* Manage your comic collection
  * Subscribe to series
  * Mark issue as read
  * Add issue to collection
  * And more...

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install comicgeeks.

```bash
pip install comicgeeks
```

## Usage

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks("my_ci_session")

# search series
client.search_series("daredevil")

# get new releases
client.new_releases()

# get info about an issue
client.issue_info(3616996)
```

For more info check the documentation in [https://comicgeeks.readthedocs.io](https://comicgeeks.readthedocs.io)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## Note

This project has been set up using PyScaffold 4.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

## License
[MIT](https://choosealicense.com/licenses/mit/)
