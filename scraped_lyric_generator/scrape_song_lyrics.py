import os

from scraped_lyric_generator.cache import Cache
from scraped_lyric_generator.scraper import get_relevant_pages, get_relevant_content


SOUP_CACHE_FILE = os.path.join('..', 'data', 'soup_cache' + '.pkl')
LYRICS_CACHE_FILE = os.path.join('..', 'data', 'lyrics_cache' + '.pkl')

URL = "https://www.azlyrics.com/m/mychemicalromance.html"
SEARCH_STRING = 'mychemicalromance'


# Initialise caches
soup_cache = Cache(SOUP_CACHE_FILE)
lyrics_cache = Cache(LYRICS_CACHE_FILE)

# Get and save song lyrics
song_links = get_relevant_pages(URL, SEARCH_STRING, soup_cache)
lyrics_cache.cache = get_relevant_content(song_links, soup_cache)
lyrics_cache.save()
