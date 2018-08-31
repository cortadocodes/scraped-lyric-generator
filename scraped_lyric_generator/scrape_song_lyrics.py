import os

from scraped_lyric_generator.cache import Cache
from scraped_lyric_generator.scraper import get_relevant_pages, get_relevant_content


SOUP_CACHE_FILE = os.path.join('..', 'data', 'soup_cache' + '.pkl')
LYRICS_CACHE_FILE = os.path.join('..', 'data', 'lyrics_cache' + '.pkl')

URL = "https://www.azlyrics.com/m/mychemicalromance.html"
SEARCH_STRING = 'mychemicalromance'


def scrape_song_lyrics(soup_cache_file, lyrics_cache_file, url, search_string):
    """
    Scrape lyrics from url, paying attention only to content relating to search_string.

    :param str soup_cache_file: file to cache soup
    :param str lyrics_cache_file: file to cache lyrics
    :param str url: website to scrape
    :param str search_string: string to search for when scraping
    """
    # Initialise caches
    soup_cache = Cache(SOUP_CACHE_FILE)
    lyrics_cache = Cache(LYRICS_CACHE_FILE)

    # Get and save song lyrics
    song_links = get_relevant_pages(URL, SEARCH_STRING, soup_cache)
    lyrics_cache.cache = get_relevant_content(song_links, soup_cache)
    lyrics_cache.save()


if __name__ == '__main__':
    scrape_song_lyrics(SOUP_CACHE_FILE, LYRICS_CACHE_FILE, URL, SEARCH_STRING)
