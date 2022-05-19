from pathlib import Path

from menagerie.Items.Managers.AbstractManager import AbstractManager
from menagerie.Items.Static.StaticCSS import StaticCSS
from menagerie.Items.Static.StaticSCSS import StaticSCSS
from menagerie.Items.Static.StaticImage import StaticImage
from menagerie.Items.Static.StaticItem import StaticItem
from menagerie.Items.Static.StaticJS import StaticJS
from menagerie.utils.str_util import remove_preceding_slash


class StaticManager(AbstractManager):
    root_dir = 'static'
    changed_files: dict[str, str] = {}
    item_types = (StaticJS, StaticCSS, StaticSCSS, StaticImage, StaticItem)

    def __init__(self, site_info) -> None:
        super(StaticManager, self).__init__(site_info)
        self.root_dir = Path(self.gen.settings['paths', 'static'])
        self.gen.shared_info['static_map'] = {}
        self.gen.shared_info['image_sizes'] = {}
        self.gen.shared_info['static_filter'] = self.get_static
        self.gen.shared_info['external_resolver_filter'] = self.external_or_static

    def initialize(self):
        for item in self.items:
            item.initialize()
            if hasattr(item,
                       'out_extension') and item.out_extension is not None and item.out_extension not in item.extensions:
                self.gen.shared_info['static_map'][str(item.in_path.as_posix())] = ''.join(item.out_path.suffixes)

    def generate(self):
        self.gen.settings['out_dir'].mkdir(parents=True, exist_ok=True)
        for item in self.items:
            item.generate()

    def external_or_static(self, link: str) -> str:
        if link.startswith('http') or link.startswith('file'):
            return link
        else:
            return self.gen.shared_info['static_filter'](remove_preceding_slash(link))

    def get_static(self, rel_path: str) -> str:
        path = rel_path
        if rel_path in self.gen.shared_info['static_map'].keys():
            path = Path(rel_path).with_suffix(self.gen.shared_info['static_map'].get(rel_path)).as_posix()
        return self.gen.settings['url_prefix'] + str(path)
