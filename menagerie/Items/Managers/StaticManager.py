from os import getenv
from pathlib import Path

from menagerie.Items.Managers.AbstractManager import AbstractManager
from menagerie.Settings import Settings
from menagerie.Items.Static.StaticItem import StaticItem
from menagerie.Items.Static.StaticImage import StaticImage


class StaticManager(AbstractManager):

    changed_files: dict[str, str] = {}
    item_types = (StaticImage, StaticItem)

    @classmethod
    def setup(cls) -> None:
        super(AbstractManager, self).setup()
        cls.root_dir = Path(Settings.folders['static'])

    @classmethod
    def initialize(cls):
        pass

    @classmethod
    def generate(cls):
        for item in items:
            item.generate()

    @classmethod
    def get_static(cls, rel_path: str) -> str:
        return Settings.url_prefix + cls.changed_files.get(rel_path, rel_path)
