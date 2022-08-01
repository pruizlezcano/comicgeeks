# Examples

## Search series

```python
from comicgeeks import Comic_Geeks

comic_geeks = Comic_Geeks()
series = comic_geeks.search_series("Daredevil")
```

```{admonition} Return

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
```

## Get new releases

```python
from comicgeeks import Comic_Geeks

comic_geeks = Comic_Geeks()
series = comic_geeks.new_releases()
```

```{admonition} Return

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
```

## Get individual series

```python
from comicgeeks import Comic_Geeks

comic_geeks = Comic_Geeks()
series = comic_geeks.series_info(150065)
```

```{admonition} Return

   .. code-block:: json

    {
      "series_id": "150065",
      "name": "Beta Ray Bill",
      "publisher": "Marvel Comics",
      "description": "<p>Beta Ray Bill is tired of playing second fiddle to Thor – and with Beta Ray’s famous hammer Stormbreaker recently destroyed at the new All-Father’s hands, tensions are higher than ever. The mighty Korbinite must strike out in search of a new weapon… and a new destiny. Assuming he can first defeat a Knullified Fin Fang Foom! Joined by colorist Mike Spicer, Daniel Warren Johnson will take Beta Ray Bill on a journey beyond the shadow of a god!</p>",
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
      "url": "/comics/series/150065/beta-ray-bill",
      "cover": "https://s3.amazonaws.com/comicgeeks/series/150065.jpg?1619183332"
    }
```

## Get individual issue

```python
from comicgeeks import Comic_Geeks

comic_geeks = Comic_Geeks()
series = comic_geeks.issue_info(3616996)
```

```{admonition} Return

   .. code-block:: json

    {
      "issue_id": "3616996",
      "character_credits": [
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>",
          "<Character object at 0x00000...>"
      ],
      "cover": {
          "name": "Daredevil #8",
          "image": "https://s3.amazonaws.com/comicgeeks/comics/covers/large-3616996.jpg?1629150053"
      },
      "community": {"pull": "43", "collect": "1,159", "readlist": "1,289", "wishlist": "195", "rating": "96"},
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
          {"role": "writer, cover artist", "Creator": "<Creator object at 0x00000...>"},
          {"role": "penciller", "Creator": "<Creator object at 0x00000...>"},
          {"role": "inker", "Creator": "<Creator object at 0x00000...>"}
          {"role": "colorist", "Creator": "<Creator object at 0x00000...>"},
          {"role": "letterer", "Creator": "<Creator object at 0x00000...>"},
          {"role": "variant cover artist", "Creator": "<Creator object at 0x00000...>"},
          {"role": "variant cover artist", "Creator": "<Creator object at 0x00000...>"},
          {"role": "variant cover artist", "Creator": "<Creator object at 0x00000...>"},
          {"role": "assistant editor", "Creator": "<Creator object at 0x00000...>"},
          {"role": "editor", "Creator": "<Creator object at 0x00000...>"},
          {"role": "executive editor", "Creator": "<Creator object at 0x00000...>"},
          {"role": "editor-in-chief", "Creator": "<Creator object at 0x00000...>"}
      ],
      "price": "$3.99",
      "publisher": "Marvel Comics",
      "pagination": {
          "prev": "<Issue object at 0x00000...>",
          "series": "<Series object at 0x00000...>",
          "next": "<Issue object at 0x00000...>"
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
      ]
    }
```
