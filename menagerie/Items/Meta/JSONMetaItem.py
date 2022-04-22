from json_minify import json_minify

from menagerie.Items.Meta.MetaItem import MetaItem
from menagerie.Items.MinifiedItemMixin import MinifiedItemMixin


class JSONMetaItem(MinifiedItemMixin, MetaItem):
    minify_key = 'json'

    def minify(self, content: str) -> str:
        return json_minify(content)
