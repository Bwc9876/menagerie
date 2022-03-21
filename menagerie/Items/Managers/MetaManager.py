from pathlib import Path

from menagerie.Items.Managers.AbstractManager import AbstractManager
from menagerie.Items.Managers.StaticManager import StaticManager
from menagerie.Items.Meta.MetaItem import MetaItem
from menagerie.Items.Meta.XMLMetaItem import XMLMetaItem
from menagerie.Items.Meta.JSONMetaItem import JSONMetaItem


class MetaManager(AbstractManager):

    item_types = (MetaItem, XMLMetaItem)
    items: list[MetaItem] = []
    root_dir = ''

    @classmethod
    def find(cls):
        pass

    @classmethod
    def initialize(cls):
        cls.items = (
            XMLMetaItem(cls, Path('sitemap.jinja2'), 'xml'),
            XMLMetaItem(cls, Path('browserconfig.jinja2'), 'xml'),
            JSONMetaItem(cls, Path('manifest.jinja2'), 'webmanifest'),
            MetaItem(cls, Path('robots.jinja2'), 'txt'),
        )

    @classmethod
    def generate(cls):
        cls.base_env.globals['pages'] = cls.site_info['pages']
        cls.base_env.filters['static'] = StaticManager.get_static
        for item in cls.items:
            item.generate()
