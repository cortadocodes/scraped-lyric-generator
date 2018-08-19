import os
import pickle


class Cacher:
    def __init__(self, path, cache=None, refresh_cache=False):
        self.path = path
        self.cache = cache
        self.refresh_cache = refresh_cache
        self.initialise()

    def initialise(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                try:
                    self.cache = pickle.load(f)
                except EOFError:
                    self.cache = {}
        else:
            self.cache = {}

    def insert_item(self, identifier, item):
        self.cache[identifier] = item

    def get_item(self, identifier):
        return self.cache[identifier]

    def save(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.cache, f)
