from pathlib import Path

from menagerie.Items.Managers.AbstractManager import AbstractManager
from menagerie.Items.Static.StaticImage import StaticImage
from menagerie.Items.Static.StaticItem import StaticItem
from menagerie.Settings import Settings


class StaticManager(AbstractManager):
    changed_files: dict[str, str] = {}
    item_types = (StaticImage, StaticItem)

    @classmethod
    def setup(cls) -> None:
        super(StaticManager, cls).setup()
        cls.root_dir = Path(Settings['paths', 'static'])

    @classmethod
    def initialize(cls):
        for item in cls.items:
            item.initialize()

    @classmethod
    def generate(cls):
        Path(Settings['out_dir'], cls.root_dir).mkdir(parents=True, exist_ok=True)
        for item in cls.items:
            item.generate()

    @classmethod
    def get_static(cls, rel_path: str) -> str:
        return Settings['url_prefix'] + cls.changed_files.get(rel_path, rel_path)
