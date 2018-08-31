import os

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from scraped_lyric_generator.cache import Cache


LYRICS_CACHE_FILE = os.path.join('..', 'data', 'lyrics_cache' + '.pkl')


def produce_all_lyrics_word_cloud(lyrics_cache_file):
    """
    Combine all lyrics to produce an aggregate word cloud.

    :param Cache lyrics_cache_file: cached lyrics
    """
    # Get scraped lyrics
    lyrics_cache = Cache(lyrics_cache_file)
    songs = lyrics_cache.cache

    # Put all lyrics together for aggregate analysis
    all_lyrics = []
    for song in songs.values():
        lyrics = song.replace('\\r', '').replace('\\n', '').lower().split()
        all_lyrics += lyrics

    # Create and plot wordcloud
    wordcloud = WordCloud(max_font_size=55).generate(' '.join(all_lyrics))
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    produce_all_lyrics_word_cloud(LYRICS_CACHE_FILE)
