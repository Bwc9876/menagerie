
from rjsmin import jsmin

from menagerie.Items.Meta.MetaItem import MetaItem
from menagerie.Items.MinifiedItemMixin import MinifiedItemMixin


class JSMetaScript(MinifiedItemMixin, MetaItem):

    extensions = ('js',)
    out_extension = 'min.js'
    minify_key = 'js'

    def minify(self, content: str) -> str:
        return jsmin(content)


