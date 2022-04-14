from abc import ABC

from menagerie.Items.AbstractItem import AbstractItem

__all__ = ('MinifiedItemMixin',)


class MinifiedItemMixin(AbstractItem, ABC):
    byte_mode = False
    minify_key: str = None

    def minify(self, content: str) -> str:
        raise NotImplementedError()

    def save(self, new_content: str) -> None:
        if self.manager.gen.settings['minify'][self.minify_key] is True:
            super(MinifiedItemMixin, self).save(self.minify(new_content))
        else:
            super(MinifiedItemMixin, self).save(new_content)
