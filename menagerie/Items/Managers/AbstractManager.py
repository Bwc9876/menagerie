from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader

from menagerie.Items.AbstractItem import AbstractItem

__all__ = ('AbstractManager',)

from menagerie.SiteGen import SiteGen


class AbstractManager(ABC):
    item_types: tuple
    items: list[AbstractItem] = []
    root_dir: Path
    base_env: Environment = Environment(loader=PackageLoader('menagerie.base_templates', '.'))
    gen: SiteGen = None

    def __new__(cls, *args, **kwargs):
        if cls.root_dir is None:
            raise NotImplementedError("Root Dir is None")
        if cls.item_types is None:
            raise NotImplementedError("Item Types is None")
        return super(AbstractManager, cls).__new__(cls)

    def __init__(self, site_gen: SiteGen):
        self.items = []
        self.gen = site_gen
        self.base_env.globals.update({
            'settings': self.gen.settings,
            'gen_time': datetime.now().strftime("%d/%m/%Y")
        })
        self.base_env.filters.update({
            'full_url': lambda relative: self.gen.settings['base_url'] + (
                relative[1:] if len(relative) > 1 and relative[0] == "/" else relative)
        })

    def find(self):
        matches = []
        for item_type in self.item_types:
            for ext in item_type.extensions:
                for path in Path(self.gen.settings['content_dir'], self.root_dir).glob(f'**/*.{ext}'):
                    if str(path) not in matches:
                        self.items.append(item_type(self, path.relative_to(self.gen.settings['content_dir'])))
                        matches.append(str(path))

    def get_items(self):
        return self.items

    @abstractmethod
    def initialize(self):
        pass

    def generate(self):
        raise NotImplementedError()