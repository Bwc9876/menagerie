from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from Items.Managers.AbstractManager import AbstractManager
from Items.Managers.StaticManager import StaticManager
from Items.Pages.AbstractPage import AbstractPage
from Items.Pages.HTMLPage import HTMLPage
from Items.Pages.MDPage import MDPage
from Settings import Settings


class PageManager(AbstractManager):

    root_dir = None
    item_types: AbstractPage = (MDPage, HTMLPage)
    items: list[AbstractPage] = []
    context: dict[str, object] = {

    }

    env: Environment = Environment(loader=FileSystemLoader(Settings.content_dir))
    router: dict[str, str] = {}

    @classmethod
    def setup(cls) -> None:
        super(AbstractManager, self).setup()
        cls.root_dir = Path(Settings.folders['pages'])

    @classmethod
    def initialize(cls):
        for item in cls.items:
            item.initialize()
        cls.router = {p.meta['title']: str(p.out_path) for p in cls.items}

    @classmethod
    def route(cls, title: str) -> str:
        return cls.router.get(title, "#")

    @classmethod
    def generate(cls):
        Path(Settings.out_dir, cls.root_dir).mkdir(parents=True, exist_ok=True)
        filters = {
            'route': cls.route,
            'static': StaticManager.get_static
        }
        da_globals = {
            'pages': cls.items,
        }
        cls.base_env.filters.update(filters)
        cls.base_env.globals.update(da_globals)
        cls.env.filters.update(cls.base_env.filters)
        cls.env.globals.update(cls.base_env.globals)
        for item in cls.items:
            item.generate()
