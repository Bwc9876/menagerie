import importlib.resources as pkg_resources
from json import loads, load, JSONDecodeError
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from markdown import Markdown

from menagerie import schemas
from menagerie.Items.Managers.AbstractManager import AbstractManager
from menagerie.Items.Pages.AbstractPage import AbstractPage
from menagerie.utils.str_util import pretty_title
from menagerie.Items.Pages.HTMLPage import HTMLPage
from menagerie.Items.Pages.MDPage import MDPage
from menagerie.Items.Pages.Schema.JSONSchema import JSONSchema
from menagerie.Items.Pages.Schema.XMLSchema import XMLSchema
from menagerie.utils.logger import Logger


class NavItem:

    def __init__(self, content: str | list['NavItem'], is_folder: bool, meta: dict[str, object]):
        self.is_folder = is_folder
        self.titles = []
        self.meta = meta
        if is_folder:
            self.content = []
        else:
            self.content = content

    def add_item(self, nav_item: 'NavItem') -> None:
        if self.is_folder:
            self.content.append(nav_item)

    def iter_items(self) -> None:
        for page in sorted(self.content, key=lambda p: p.meta['sort_priority'], reverse=True):
            yield page

    def setup_titles(self) -> None:
        if self.is_folder:
            self.titles = [str(p.meta['title']).lower() for p in self.content]


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
        self.group_schema = loads(pkg_resources.read_text(schemas, 'folder_schema.json', encoding='utf-8'))

    def find(self):
        super(PageManager, self).find()

    def initialize(self):
        for item in self.items:
            item.initialize()
        self.router = {p.meta['title'].lower(): str(p.out_path.relative_to(self.gen.settings['out_dir']).as_posix()) for
                       p in self.items}
        self.gen.shared_info['pages'] = filter(lambda i: i.meta['hide_in_nav'] is False, self.items)
        self.filter_md = Markdown(extensions=['extra'], output_format='html5')

    def route(self, title: str) -> str:
        return self.gen.settings['url_prefix'] + self.router.get(title.lower(), "#")

    def make_nav_item_from_page(self, page: AbstractPage) -> NavItem:
        return NavItem(self.route(page.meta['title']), False, page.meta)

    def generate_nav_items(self) -> list[NavItem]:
        root_pages = []
        groups: dict[str, NavItem] = {}
        for page in filter(lambda p: p.meta['hide_in_nav'] is not True, self.items):
            if page.in_path.parent.name != '':
                if page.in_path.parent.name in groups.keys():
                    groups[page.in_path.parent.name].add_item(self.make_nav_item_from_page(page))
                else:
                    group_config_path = Path(page.get_path_to_open().parent, '_folder.json')
                    group_meta = {
                        'title': pretty_title(group_config_path.parent.name),
                        'sort_priority': 30
                    }
                    if group_config_path.exists():
                        try:
                            group_config = loads(group_config_path.read_text(encoding='utf-8'))
                            validate(group_config, self.group_schema)
                            group_meta.update(group_config)
                        except JSONDecodeError as jde:
                            Logger.log_error(f"Couldn't parse config for {group_config_path.name} : {str(jde)}")
                        except ValidationError as ve:
                            Logger.log_error(f"Invalid folder config for {group_config_path.name} : {str(ve)}")
                    new_group = NavItem([], True, group_meta)
                    new_group.add_item(self.make_nav_item_from_page(page))
                    groups[group_config_path.parent.name] = new_group
            else:
                new_page = self.make_nav_item_from_page(page)
                root_pages.append(new_page)
        for group in groups.values():
            group.setup_titles()
        return sorted(list(groups.values()) + root_pages, key=lambda n: n.meta['sort_priority'], reverse=True)

    def generate(self):
        self.gen.settings['out_dir'].mkdir(parents=True, exist_ok=True)
        nav_items = self.generate_nav_items()
        if self.gen.settings['cache_enabled']:
            self.gen.cache.check_for_meta_change(nav_items)
        filters = {
            'route': self.route,
            'static': self.gen.shared_info['static_filter'],
            'upper_first': lambda x: x[0].upper() + x[1:],
            'simple_md': lambda md: self.filter_md.convert(md)
        }
        da_globals = {
            'nav_items': nav_items,
        }
        self.base_env.filters.update(filters)
        self.base_env.globals.update(da_globals)
        self.env.filters.update(self.base_env.filters)
        self.env.globals.update(self.base_env.globals)
        for item in self.items:
            item.generate()
