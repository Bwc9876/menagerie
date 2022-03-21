from abc import ABC

from menagerie.Items.AbstractItem import AbstractItem

__all__ = ('MinifiedItemMixin',)


class MinifiedItemMixin(AbstractItem, ABC):
    byte_mode = False

    def minify(self, content: str) -> str:
        raise NotImplementedError()

    def save(self, new_content: str) -> None:
        super(MinifiedItemMixin, self).save(self.minify(new_content))
