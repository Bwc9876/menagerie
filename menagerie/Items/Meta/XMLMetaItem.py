from htmlmin import minify

from menagerie.Items.MinifiedItemMixin import MinifiedItemMixin
from menagerie.Items.Meta.MetaItem import MetaItem
from menagerie.Items.Pages.AbstractPage import MINIFY_SETTINGS


class XMLMetaItem(MinifiedItemMixin, MetaItem):

    out_extension = 'xml'
    minify_key = 'xml'

    def minify(self, content: str) -> str:
        return minify(content, **MINIFY_SETTINGS)

