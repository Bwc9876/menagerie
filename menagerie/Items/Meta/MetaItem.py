from pathlib import Path

from menagerie.Items.AbstractItem import AbstractItem


class MetaItem(AbstractItem):

    byte_mode = False
    extensions = ('*',)

    def __init__(self, manager, path: Path, out_ext):
        self.out_extension = out_ext
        super(MetaItem, self).__init__(manager, path)

    def get_path_to_open(self) -> Path:
        return Path('base_templates/meta_files/', self.in_path)

    def initialize(self) -> None:
        pass

    def transform(self, content: str) -> str:
        return self.manager.base_env.from_string(content).render()
