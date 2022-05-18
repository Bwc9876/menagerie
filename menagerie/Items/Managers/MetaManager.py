from pathlib import Path

from menagerie.Items.Managers.AbstractManager import AbstractManager
from menagerie.Items.Meta.JSONMetaItem import JSONMetaItem
from menagerie.Items.Meta.JSMetaItem import JSMetaScript
from menagerie.Items.Meta.CSSMetaItem import CSSMetaItem
from menagerie.Items.Meta.MetaItem import MetaItem
from menagerie.Items.Meta.XMLMetaItem import XMLMetaItem


class MetaManager(AbstractManager):
    item_types = (MetaItem, XMLMetaItem)
    root_dir = ''

    def find(self):
        pass

    def initialize(self):
        self.items = (
            XMLMetaItem(self, Path('sitemap.jinja2'), 'xml'),
            XMLMetaItem(self, Path('browserconfig.jinja2'), 'xml'),
            JSONMetaItem(self, Path('manifest.jinja2'), 'webmanifest'),
            JSMetaScript(self, Path('base.js'), 'min.js'),
            JSMetaScript(self, Path('schema.js'), 'min.js'),
            CSSMetaItem(self, Path('schema.css'), 'min.css'),
            MetaItem(self, Path('robots.jinja2'), 'txt'),
        )

    def generate(self):
        self.base_env.globals['pages'] = self.gen.shared_info['pages']
        self.base_env.filters['static'] = self.gen.shared_info['static_filter']
        for item in self.items:
            item.generate()
