from PIL import Image

from menagerie.Items.Static import StaticItem
from menagerie.Settings import Settings

class StaticImage(StaticItem):

    extensions = ('png', 'jpg', 'jpeg', 'webp')
    __sizes: dict[str, tuple[int]] = {}

    @classmethod
    def get_size(cls, path: str) -> tuple[int]:
        return cls.__sizes.get(path, (100, 100))

    def initialize(self) -> None:
        with Image.open(self.get_path_to_open()) as img:
            self.__sizes[str(self.out_path.relative_to(Settings.out_dir).as_posix())] = img.size
