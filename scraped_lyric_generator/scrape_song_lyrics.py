from scraped_lyric_generator.get_relevant_pages import get_relevant_pages


URL = "https://www.azlyrics.com/m/mychemicalromance.html"
SEARCH_STRING = 'mychemicalromance'


song_links = get_relevant_pages(URL, SEARCH_STRING)
