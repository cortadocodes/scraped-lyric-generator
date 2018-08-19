import os

from scraped_lyric_generator.scraper import get_relevant_pages, get_relevant_content


CACHE_FILE = os.path.join('..', 'data', 'cache' + '.pkl')
URL = "https://www.azlyrics.com/m/mychemicalromance.html"
SEARCH_STRING = 'mychemicalromance'


song_links = get_relevant_pages(URL, SEARCH_STRING, CACHE_FILE)
songs = get_relevant_content(song_links)
