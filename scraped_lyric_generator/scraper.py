import os
import pickle
import requests
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


def get_relevant_pages(url, search_string, cache_file):
    """
    Given the url for a page, get a dictionary of child page names and
    their links if they contain the search_string. Keep a cache in
    cache_file of the scraped content used to do this so the server
    isn't over-requested and doesn't block the scraper.

    :param str url: URL of the main page
    :param str search_string: string to look for in each link
    :param str cache_file: path to the cache file

    :return dict: the page names and their links
    """

    base_url = get_base_url(url)
    soup = get_soup(url, cache_file)
    relevant_pages = get_relevant_links(soup, search_string, base_url)
    return relevant_pages


def get_base_url(url):
    """
    Get the full base URL for an arbitrarily-long url, including its
    scheme (e.g. http://)

    :param str url: the full URL

    :return str: the base URL including scheme
    """

    separator = '://'
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + separator + parsed_url.netloc
    return base_url


def get_soup(url, cache_file, refresh_cache=False):
    """
    Scrape the url and return its contents as a BeautifulSoup object. If
    the url has already been scraped and is cached, return the contents
    of the cache instead.

    :param str url: the webpage to be scraped
    :param str cache_file: path to the cache file
    :param bool refresh_cache: if true, scrape url again, even if its
        contents are in the cache

    :return bs4.BeautifulSoup: the HTML contents of the webpage in an
        easily crawlable form
    """

    # Load cache if it exists
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            try:
                cache = pickle.load(f)
            except EOFError:
                cache = {}
    else:
        cache = {}

    # Load the scraped content from the cache if it exists there
    if (url in cache.keys() and not refresh_cache):
        content = cache[url]

        # If the cache contains no content for the URL, then scrape anyway
        if content is None:
            content = try_scraping(url, timeout=5)
            if content is not None:
                cache[url] = content

    # If the URL doesn't exis in the cache, scrape the webpage
    else:
        content = try_scraping(url, timeout=5)
        if content is not None:
            cache[url] = content

    # Save the cache
    with open(cache_file, 'wb') as f:
        pickle.dump(cache, f)

    # Create the soup object
    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        return soup


def try_scraping(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        content = response.text
        return content

    except requests.exceptions.ConnectionError:
        message = 'Connection error for url {} (server may have blocked scraper)'
        print(message.format(url))


def get_relevant_links(soup, search_string, base_url):
    """
    Take the soup from a webpage and return all of its links containing
    the search_string.

    :param bs4.BeautifulSoup soup: the soup from the webpage of interest
    :param str search_string: the string of interest
    :param str base_url: e.g. 'http://www.example.com'

    :return dict: page names and their corresponding URLs
    """

    if soup is not None:
        # Get all links
        link_objects = soup.find_all('a')
        relevant_links = {}

        # Store links containing the search_string
        for link_object in link_objects:
            link = link_object.get('href')
            if link is not None:
                if search_string in link:
                    page_name = get_page_name(link)
                    full_link = urljoin(base_url, link)
                    relevant_links[page_name] = full_link

        return relevant_links


def get_page_name(link):
    """
    Extract the page name from a URL.

    :param str link: URL of a webpage

    :return str: the name of the webpage (the final part of the URL, with
        extension removed
    """

    page_name = link.split('/')[-1].split('.')[0]
    return page_name


def get_relevant_content(relevant_links, cache_file):
    """
    Scrape lots of webpages for their "relevant content" given a list of
    links. Only scrape if the pages' contents are not already in the cache.

    :param dict relevant_links: page names with their corresponding links
    :param str cache_file: path to the cache file

    :return dict: page names with their corresponding relevant content
    """

    relevant_content = {}
    if relevant_links is not None:
        for page_name, link in relevant_links.items():
            soup = get_soup(link, cache_file)
            if soup is not None:
                content = soup.body.find_all('div')[21].text
                relevant_content[page_name] = content

        return relevant_content
