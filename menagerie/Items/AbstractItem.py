from abc import ABC
from pathlib import Path

from Settings import Settings
from menagerie.utils.logger import Logger


__all__ = ('AbstractItem',)


class AbstractItem(ABC):
    content: str | bytes
    root_dir: Path
    byte_mode: bool = False
    in_path: Path
    out_path: Path
    extensions: tuple
    out_extension: str

    def __new__(cls, *args, **kwargs):
        if cls.extensions is None:
            raise NotImplementedError("extensions are not implemented")
        if cls.out_extension is None:
            raise NotImplementedError('out_extension is not implemented')
        return super(AbstractItem, cls).__new__(cls)

    def __init__(self, manager, path: Path):
        self.manager = manager
        self.in_path = path.relative_to(self.manager.root_dir)
        self.out_path = Path(Settings.out_dir, self.manager.root_dir, Path(self.manager.root_dir, self.in_path).relative_to(Path(self.manager.root_dir))).with_suffix(f'.{self.out_extension}')

    def get_path_to_open(self) -> Path:
        return Path(Settings.content_dir, self.manager.root_dir, self.in_path)

    def get_content(self) -> str | byte:
        with self.get_path_to_open().open(mode='rb' if self.byte_mode else 'r') as file:
            return file.read()

    def generate(self) -> None:
        Logger.log_info("Building: " + str(self.in_path.as_posix()) + ' -> ' + str(self.out_path.as_posix()))
        self.save(self.transform(self.content))

    def initialize(self) -> None:
        raise NotImplementedError()

    def transform(self, content: str | bytes) -> str | bytes:
        return content

    def save(self, new_content: str | bytes) -> None:
        with self.out_path.open(mode='wb+' if self.byte_mode else 'w+') as file:
            file.write(new_content)
