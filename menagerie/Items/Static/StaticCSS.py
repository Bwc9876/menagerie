from rcssmin import cssmin

from menagerie.Items.Static.StaticItem import StaticItem
from menagerie.Items.MinifiedItemMixin import MinifiedItemMixin


class StaticCSS(MinifiedItemMixin, StaticItem):

    extensions = ('css',)
    out_extension = 'min.css'

    def minify(self, content: str) -> str:
        return cssmin(content)
