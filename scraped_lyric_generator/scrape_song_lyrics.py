import requests
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


URL = "https://www.azlyrics.com/m/mychemicalromance.html"
SEARCH_STRING = 'mychemicalromance'


def get_base_url(url):
    separator = '://'
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + separator + parsed_url.netloc
    return base_url


def get_soup(url):
    # Get soup (content) from URL
    response = requests.get(url, timeout=5)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def get_relevant_links(soup, search_string, base_url):
    # Get all links
    link_objects = soup.find_all('a')
    relevant_links = []

    # Store links containing the search_string
    for link_object in link_objects:
        link = link_object.get('href')
        if link is not None:
            if search_string in link:
                full_link = urljoin(base_url, link)
                relevant_links.append(full_link)

    return relevant_links


base_url = get_base_url(URL)
soup = get_soup(URL)
song_links = get_relevant_links(soup, SEARCH_STRING, base_url)
