# Scrapy

A basic link scrapper and retriever

## Installation

```
pip install -r requirements.txt
```

## Usage

### Working Sample

```python
python3 Scrapy.py
```

It will fill the data folder with pdf from a pre-filled website

### Integration in your own code

```python
from Scrapy import Scrapper

# Decalre the scrapper Object
my_sample_scrapper = Scrapper("https://my-scrapping-url.com", "my/storage/folder")

# Scrap all links into the webpage
links = my_sample_scrapper.scrap_links_in_url()

# Retrieve all these links into my/storage/folder
my_sample_scrapper.retrieve_urls(links)

```
