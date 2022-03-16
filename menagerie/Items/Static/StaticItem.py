from menagerie.Items.AbstractItem import AbstractItem


class StaticItem(AbstractItem):

    extensions = ('*',)
    
    def initialize(self) -> None:
        pass

