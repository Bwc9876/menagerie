from rcssmin import cssmin

from menagerie.Items.Meta.MetaItem import MetaItem
from menagerie.Items.MinifiedItemMixin import MinifiedItemMixin


class CSSMetaItem(MinifiedItemMixin, MetaItem):

    minify_key = 'css'
    out_extension = 'min.css'
    extensions = ('css',)

    def minify(self, content: str) -> str:
        return cssmin(content)
