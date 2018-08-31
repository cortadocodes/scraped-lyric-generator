import os

from scraped_lyric_generator.cache import Cache
from scraped_lyric_generator.scraper import get_relevant_pages, get_relevant_content


CACHE_FILE = os.path.join('..', 'data', 'cache' + '.pkl')
URL = "https://www.azlyrics.com/m/mychemicalromance.html"
SEARCH_STRING = 'mychemicalromance'


# Initialise cache
cache = Cache(CACHE_FILE)

song_links = get_relevant_pages(URL, SEARCH_STRING, cache)
songs = get_relevant_content(song_links, cache)
