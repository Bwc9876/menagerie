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
    def find(cls):
        for path in Path(Settings.content_dir, cls.root_dir).glob('**/*.*'):
            print(path)
            for item_type in cls.item_types:
                if path.suffix[1:] in item_type.extensions:
                    cls.items.append(item_type(cls, path.relative_to(Settings.content_dir)))
                    break

    @classmethod
    def initialize(cls):
        raise NotImplementedError()

    @classmethod
    def generate(cls):
        raise NotImplementedError()
