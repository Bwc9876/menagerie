from PIL import Image

from menagerie.Items.Static.StaticItem import StaticItem


class StaticImage(StaticItem):
    extensions = ('png', 'jpg', 'jpeg', 'webp', 'gif')
    out_extension = None

    def initialize(self) -> None:
        with Image.open(self.get_path_to_open(), mode='r') as img:
            self.manager.gen.shared_info['image_sizes'][str(self.out_path.relative_to(self.manager.gen.settings['out_dir']).as_posix())] = img.size
