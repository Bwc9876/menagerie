class SiteGen:

    def __init__(self, settings, managers):
        self.settings = settings
        self.shared_info = {}
        self.managers = [manager(self) for manager in managers]

    def find(self):
        for manager in self.managers:
            manager.find()

    def initialize(self):
        for manager in self.managers:
            manager.initialize()

    def generate(self):
        for manager in self.managers:
            manager.generate()
