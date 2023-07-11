# Examples

## Search

### Search series

```python
from comicgeeks import Comic_Geeks

comic_geeks = Comic_Geeks()
series = comic_geeks.search_series("Daredevil")
```

````{admonition} Return
```{eval-rst}
  .. code-block:: none

    [
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      94 more...
    ]

````

### Search creator

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks()
creators = client.search_creator("Chip")
```

````{admonition} Return
```{eval-rst}
   .. code-block:: none

    [
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      <Series object at 0x00000...>,
      94 more...
    ]
````

### Search character

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks()
characters = client.search_character("Spider-man")
```

````{admonition} Return
```{eval-rst}
   .. code-block:: none

    [
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      <Character object at 0x00000...>,
      40 more...
    ]
````

### Get new releases

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks()
issues = client.new_releases()
```

````{admonition} Return
```{eval-rst}
   .. code-block:: none

    [
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      <Issue object at 0x00000...>,
      73 more...
    ]
````

## Get by id

### Get series

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks()
series = client.series_info(150065)
```

````{admonition} Return
```{eval-rst}
   .. code-block:: json

    {
      "series_id": 150065,
      "name": "Beta Ray Bill",
      "publisher": "Marvel Comics",
      "description": "Beta Ray Bill is tired of playing second fiddle to Thor – and with Beta Ray’s famous hammer Stormbreaker recently destroyed at the new All-Father’s hands, tensions are higher than ever. The mighty Korbinite must strike out in search of a new weapon… and a new destiny. Assuming he can first defeat a Knullified Fin Fang Foom! Joined by colorist Mike Spicer, Daniel Warren Johnson will take Beta Ray Bill on a journey beyond the shadow of a god!",
      "start_year": 2021,
      "end_year": 2021,
      "issues": [
          "<Issue object at 0x00000..>",
          "<Issue object at 0x00000..>",
          "<Issue object at 0x00000..>",
          "<Issue object at 0x00000..>",
          "<Issue object at 0x00000..>"
      ],
      "issue_count": 5,
      "trade_paperbacks": [
          "<Trade_Paperback object at 0x00000..>",
      ],
      "trade_paperback_count": 1,
      "url": "/comics/series/150065/beta-ray-bill",
      "cover": "https://s3.amazonaws.com/comicgeeks/series/150065.jpg?1619183332",
      "user": { // Only valid if ci_session is provided
        "pull": "None",
        "owned": "None",
        "read": "None"
      }
    }
````

### Get issue

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks()
issue = client.issue_info(3616996)
```

````{admonition} Return
```{eval-rst}
   .. code-block:: json

    {
      "issue_id": 3616996,
      "character_credits": [
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>"
      ],
      "cover": {
        "name": "Daredevil #8",
        "image": "https://s3.amazonaws.com/comicgeeks/comics/covers/large-3616996.jpg?1629150053"
      },
      "community": {
        "pull": "Unknown",
        "collect": 1177,
        "readlist": 1350,
        "wishlist": 202,
        "rating": 96
      },
      "description": "NO DEVILS, ONLY GOD, PART 3\xa0With Daredevil still missing, his shadow looms large over Hell’s Kitchen…and ordinary citizens are starting to feel his absence. Detective Cole North may think he’s stopped Daredevil, but there are bigger problems coming his way!\xa0LEGACY #620",
      "details": {
        "format": "comic",
        "page_count": "28 pages",
        "upc": "75960609142300811",
        "distributor_sku": "may190864"
      },
      "name": "No Devils, Only God, Part 3",
      "number": "8",
      "person_credits": [
        {
          "role": "writer, cover artist",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "penciller",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "inker",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "colorist",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "letterer",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "variant cover artist",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
           "role": "variant cover artist",
           "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "variant cover artist",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "assistant editor",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "editor",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "executive editor",
          "Creator": "<classes.Creator object at 0x00000...>"
        },
        {
          "role": "editor-in-chief",
          "Creator": "<classes.Creator object at 0x00000...>"
        }
      ],
      "price": 3.99,
      "publisher": "Marvel Comics",
      "pagination": {
        "prev": "<classes.Issue object at 0x00000...>",
        "series": "<classes.Series object at 0x00000...>",
        "next": "<classes.Issue object at 0x00000...>"
      },
      "store_date": 1563314400,
      "url": "/comic/3616996/daredevil-8",
      "variant_covers": [
        {
          "name": "Daredevil #8 2nd Printing",
          "url": "/comic/3616996/daredevil-8?variant=8785071",
          "image": "https://s3.amazonaws.com/comicgeeks/comics/covers/medium-8785071.jpg?1610895121"
        },
        {
          "name": "Daredevil #8 Lee Garbett Carnage-ized Variant",
          "url": "/comic/3616996/daredevil-8?variant=5800290",
          "image": "https://s3.amazonaws.com/comicgeeks/comics/covers/medium-5800290.jpg?1607293889"
        }
      ],
      "user": { // Only valid if ci_session is provided
        "pull": "None",
        "collect": "None",
        "readlist": "None",
        "wishlist": "None",
        "rating": "None"
      }
    }
````

### Get creator

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks()
creator = client.creator_info(6209)
```

````{admonition} Return
```{eval-rst}
   .. code-block:: json

    {
      "characters": [
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "<classes.Character object at 0x00000...>",
        "and many more..."
      ],
      "series": [
        "<classes.Series object at 0x00000...>",
        "<classes.Series object at 0x00000...>",
        "<classes.Series object at 0x00000...>",
        "<classes.Series object at 0x00000...>",
        "<classes.Series object at 0x00000...>",
        "and many more..."
      ],
      "creator_id": 6209,
      "description": "Steve Murray (better known under the pen name of Chip Zdarsky) is a Canadian comic book creator most known for his work with Matt Fraction in Sex Criminals\xa0as the artist and his books at Marvel such as Daredevil, The Spectacular Spider-Man and Howard the Duck.",
      "image": "https://s3.amazonaws.com/comicgeeks/people/avatars/6209.jpg?t=1604083961", "name": "Chip Zdarsky",
      "url": "/people/6209/chip-zdarsky",
      "read": "None", // Only valid if ci_session is provided
      "owned": "None", // Only valid if ci_session is provided
      "issue_count": 378
    }
````

### Get character

```python
from comicgeeks import Comic_Geeks

client = Comic_Geeks()
character = client.creator_info(6209)
```

````{admonition} Return
```{eval-rst}
  .. code-block:: json

    {
      "character_id": 11699,
      "image": "https://s3.amazonaws.com/comicgeeks/characters/avatars/11699.jpg?t=1608688306",
      "creators": [
        "<classes.Creator object at 0x00000...>",
        "<classes.Creator object at 0x00000...>"
      ],
      "description": "The lethal scarlet assassin. Elektra is Daredevil's most fearsome enemy, as well as his former lover, and most renowned assassin in the world.",
      "information": [
        {
          "key": "First Appearance",
          "value": "Daredevil #25"
        }
      ],
      "also_known_as": [],
      "series": [
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>",
        "<classes.Series object at 0x0000...>"
      ],
      "universe": "Earth-616",
      "publisher": "Marvel Comics",
      "name": "Daredevil",
      "real_name": "Elektra Natchios",
      "url": "/character/11699/daredevil",
      "read": "None", // Only valid if ci_session is provided
      "owned": "None", // Only valid if ci_session is provided
      "issue_count": 37
    }
````
