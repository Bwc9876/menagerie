from rjsmin import jsmin

from menagerie.Items.MinifiedItemMixin import MinifiedItemMixin
from menagerie.Items.Static.StaticItem import StaticItem


class StaticJS(MinifiedItemMixin, StaticItem):

    extensions = ('js',)
    out_extension = 'min.js'

    def minify(self, content: str) -> str:
        return jsmin(content)

