import os
import pickle
import requests
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


def get_relevant_pages(url, search_string, cache_file):
    base_url = get_base_url(url)
    soup = get_soup(url, cache_file)
    relevant_pages = get_relevant_links(soup, search_string, base_url)
    return relevant_pages


def get_base_url(url):
    separator = '://'
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + separator + parsed_url.netloc
    return base_url


def get_soup(url, cache_file, add_to_cache=True):
    # Load cache if it exists
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            cache = pickle.load(f)
    else:
        cache = {}

    # Load the scraped content from the cache if it exists there
    if url in cache.keys():
        content = cache[url]

    # Otherwise, get the soup from the server
    else:
        response = requests.get(url, timeout=5)
        content = response.text

        if add_to_cache:
            cache[url] = content

    # Save the cache
    with open(cache_file, 'wb') as f:
        pickle.dump(cache, f)

    # Create the soup object
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def get_relevant_links(soup, search_string, base_url):
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
    page_name = link.split('/')[-1].split('.')[0]
    return page_name
