import re
from abc import ABC
from pathlib import Path

from menagerie.Items.AbstractItem import AbstractItem
from menagerie.Items.MinifiedItemMixin import MinifiedItemMixin
from htmlmin import minify as html_minify
from jinja2.environment import Markup

__all__ = ('AbstractPage', 'MINIFY_SETTINGS')


def camel_to_pretty(raw):
    return ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', raw))


def pretty_title(raw: str) -> str:
    if '_' in raw:
        return ' '.join(x[0].upper() + x[1:] for x in raw.split('_'))
    elif any(x.isupper() for x in raw):
        if raw[0].islower():
            new_raw = raw[0].upper() + raw[1:]
        else:
            new_raw = raw
        return camel_to_pretty(new_raw)
    else:
        return raw[0].upper() + raw[1:]


MINIFY_SETTINGS = {
    'remove_empty_space': True,
    'keep_pre': True,
    'remove_optional_attribute_quotes': False
}


class AbstractPage(MinifiedItemMixin, AbstractItem, ABC):
    byte_mode = False
    out_extension = 'html'

    def __init__(self, manager, path: Path):
        super().__init__(manager, path)
        self.meta: dict[str, object] = {
            'title': None,
            'description': "No Description Provided",
            'sort_priority': 10,
            'hide_in_nav': False,
            'render_toc': True,
            'table_of_contents': None
        }

    def load_metadata(self) -> None:
        raise NotImplementedError()

    def inner_render(self, content: str) -> str:
        raise NotImplementedError()

    def initialize(self) -> None:
        self.load_metadata()
        if self.meta['title'] is None:
            self.meta['title'] = pretty_title(self.in_path.stem)

    def transform(self, content: str) -> str:
        base_template = self.manager.base_env.get_template("page_base.jinja2")
        return base_template.render(page=self, content=Markup(self.inner_render(content)), **self.manager.context)

    def minify(self, content: str) -> str:
        return html_minify(content, **MINIFY_SETTINGS)
