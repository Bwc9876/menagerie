from menagerie.Items.Managers.AbstractManager import AbstractManager


class StaticManager(AbstractManager):

    @classmethod
    def initialize(cls):
        pass

    @classmethod
    def generate(cls):
        for item in items:
            item.generate()
