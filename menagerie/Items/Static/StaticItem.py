from menagerie.Items.AbstractItem import AbstractItem


class StaticItem(AbstractItem):
    extensions = ('*',)
    byte_mode = True

    def initialize(self) -> None:
        pass
