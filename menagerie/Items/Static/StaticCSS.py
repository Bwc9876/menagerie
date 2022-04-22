from rcssmin import cssmin

from menagerie.Items.MinifiedItemMixin import MinifiedItemMixin
from menagerie.Items.Static.StaticItem import StaticItem


class StaticCSS(MinifiedItemMixin, StaticItem):
    extensions = ('css',)
    minify_key = 'css'
    out_extension = 'min.css'
    byte_mode = False

    def minify(self, content: str) -> str:
        return cssmin(content)
