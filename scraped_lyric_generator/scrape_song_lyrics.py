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


def get_links_to_relevant_pages(url, search_string):
    base_url = get_base_url(url)
    soup = get_soup(url)
    relevant_links = get_relevant_links(soup, search_string, base_url)
    return relevant_links


song_links = get_links_to_relevant_pages(URL, SEARCH_STRING)
