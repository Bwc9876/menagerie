from pathlib import Path

import importlib.resources as pkg_resources

from menagerie.Items.AbstractItem import AbstractItem
from menagerie.base_templates import meta_files


class MetaItem(AbstractItem):

    should_cache = False
    byte_mode = False
    extensions = ('*',)

    def __init__(self, manager, path: Path, out_ext):
        self.out_extension = out_ext
        super(MetaItem, self).__init__(manager, path)

    def get_content(self) -> str | bytes:
        return pkg_resources.read_text(meta_files, self.in_path)

    def initialize(self) -> None:
        pass

    def transform(self, content: str) -> str:
        return self.manager.base_env.from_string(content).render()
