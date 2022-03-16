from abc import ABC
from pathlib import Path

from jinja2 import Environment, PackageLoader

from Items.AbstractItem import AbstractItem
from Settings import Settings

__all__ = ('AbstractManager',)


class AbstractManager(ABC):

    item_types: tuple
    items: list[AbstractItem] = []
    root_dir: Path
    base_env: Environment = Environment(loader=PackageLoader('base_templates', '.'))

    def __new__(cls, *args, **kwargs):
        if cls.root_dir is None:
            raise NotImplementedError("Root Dir is None")
        if cls.item_types is None:
            raise NotImplementedError("Item Types is None")
        return super(AbstractManager, cls).__new__(*args, **kwargs)

    @classmethod
    def setup(cls):
        self.base_env.globals.update({
            'settings': Settings
        })
        self.base_env.filters.update({
            'full_url': lambda relative: Settings.base_url + (relative[1:] if relative[0] == "/" else relative)
        })

    @classmethod
    def find(cls):
        matches = []
        for item_type in cls.item_types:
            for ext in item_type.extensions:
                for str(path) in Path(Settings.content_dir, cls.root_dir).glob(f'**/*.{ext}'):
                    if path not in matches:
                        cls.items.append(item_type(cls, path.relative_to(Settings.content_dir)))
                        matches.append(str(path))

    @classmethod
    def initialize(cls):
        raise NotImplementedError()

    @classmethod
    def generate(cls):
        raise NotImplementedError()
