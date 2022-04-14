from pathlib import Path

from menagerie.Items.Managers.AbstractManager import AbstractManager
from menagerie.Items.Pages.AbstractPage import AbstractPage
from menagerie.Items.Pages.HTMLPage import HTMLPage
from menagerie.Items.Pages.MDPage import MDPage
from menagerie.Items.Pages.Schema.JSONSchema import JSONSchema
from menagerie.Items.Pages.Schema.XMLSchema import XMLSchema
from jinja2 import Environment, FileSystemLoader


class PageManager(AbstractManager):
    root_dir = 'pages'
    item_types: AbstractPage = (MDPage, HTMLPage, XMLSchema, JSONSchema)
    context: dict[str, object] = {

    }

    env: Environment = None
    router: dict[str, str] = {}

    def __init__(self, site_info) -> None:
        super(PageManager, self).__init__(site_info)
        self.env = Environment(loader=FileSystemLoader(self.gen.settings['content_dir']))
        self.root_dir = Path(self.gen.settings['paths', 'pages'])

    def initialize(self):
        for item in self.items:
            item.initialize()
        self.router = {p.meta['title']: str(p.out_path.relative_to(self.gen.settings['out_dir']).as_posix()) for p in self.items}
        self.gen.shared_info['pages'] = self.items
        self.items.sort(key=lambda p: p.meta['sort_priority'], reverse=True)

    def route(self, title: str) -> str:
        return self.gen.settings['url_prefix'] + self.router.get(title, "#")

    def generate(self):
        self.gen.settings['out_dir'].mkdir(parents=True, exist_ok=True)
        filters = {
            'route': self.route,
            'static': self.gen.shared_info['static_filter'],
            'upper_first': lambda x:   x[0].upper() + x[1:],
        }
        da_globals = {
            'pages': self.items,
        }
        self.base_env.filters.update(filters)
        self.base_env.globals.update(da_globals)
        self.env.filters.update(self.base_env.filters)
        self.env.globals.update(self.base_env.globals)
        for item in self.items:
            item.generate()
