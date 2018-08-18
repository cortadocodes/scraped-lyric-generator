import requests
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


URL = "https://www.azlyrics.com/m/mychemicalromance.html"
SEARCH_STRING = 'mychemicalromance'


parsed_url = urlparse(URL)
base_url = parsed_url.scheme + '://' + parsed_url.netloc

r = requests.get(URL, timeout=5)
content = r.text
soup = BeautifulSoup(content, 'html.parser')

# Get all links
link_objects = soup.find_all('a')

# Sift for relevant links
song_links = []
for link_object in link_objects:
    link = link_object.get('href')
    if link is not None:
        if SEARCH_STRING in link:
            full_link = urljoin(base_url, link)
            song_links.append(full_link)
