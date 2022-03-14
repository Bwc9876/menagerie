from abc import ABC

from Items.AbstractItem import AbstractItem

__all__ = ('MinifiedItemMixin',)


class MinifiedItemMixin(AbstractItem, ABC):

    byte_mode = True

    def minify(self, content: str) -> str:
        raise NotImplementedError()

    def save(self, new_content: str) -> None:
        super(MinifiedItemMixin, self).save(self.minify(new_content))

