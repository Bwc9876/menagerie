from pathlib import Path

from menagerie.utils.cache_handler import CacheHandler


class SiteGen:

    def __init__(self, settings, managers):
        self.settings = settings
        self.shared_info = {}
        self.managers = [manager(self) for manager in managers]
        self.cache = CacheHandler(Path(settings['paths']['cache']))

    def find(self):
        for manager in self.managers:
            manager.find()

    def initialize(self):
        for manager in self.managers:
            manager.initialize()

    def generate(self):
        for manager in self.managers:
            manager.generate()
