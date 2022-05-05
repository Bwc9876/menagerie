from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from menagerie.Items.Managers.AbstractManager import AbstractManager

from menagerie.utils.logger import Logger

__all__ = ('AbstractItem',)


class AbstractItem(ABC):
    should_cache: bool = True
    content: str | bytes
    root_dir: Path
    byte_mode: bool = False
    in_path: Path
    out_path: Path
    extensions: tuple
    out_extension: str
    ignore_names: list[str] = []

    def __new__(cls, *args, **kwargs):
        if cls.extensions is None:
            raise NotImplementedError("extensions are not implemented")
        return super(AbstractItem, cls).__new__(cls)

    def __init__(self, manager: 'AbstractManager', path: Path):
        self.broken: bool = False
        self.manager: 'AbstractManager' = manager
        self.in_path: Path = path.relative_to(self.manager.root_dir)
        self.out_path: Path = Path(self.manager.gen.settings['out_dir'],
                                   Path(self.manager.root_dir, self.in_path).relative_to(Path(self.manager.root_dir)))
        if hasattr(self, 'out_extension') is True and (self.out_extension is not None):
            self.out_path = self.out_path.with_suffix(f'.{self.out_extension}')

    def get_path_to_open(self) -> Path:
        return Path(self.manager.gen.settings['content_dir'], self.manager.root_dir, self.in_path)

    def get_content(self) -> str | bytes:
        kwargs = {
            'mode': 'rb' if self.byte_mode else 'r'
        }
        if self.byte_mode is False:
            kwargs['encoding'] = 'utf-8'
        with self.get_path_to_open().open(**kwargs) as file:
            return file.read()

    def generate(self) -> None:
        content = self.get_content()
        rel_path = str(self.get_path_to_open().relative_to(self.manager.gen.settings['content_dir']).as_posix())
        should_cache = self.manager.gen.settings['cache_enabled'] and (self.byte_mode is False)
        hit, hashed = self.manager.gen.cache.check_for_hit(rel_path, content) if should_cache else (False, None)
        if hit:
            Logger.log_info(".")
            self.save(self.manager.gen.cache.get_cached_output(self.out_path), minify=False)
        else:
            Logger.log_info("Building: " + str(self.in_path.as_posix()) + ' ➔ ' + str(self.out_path.as_posix()))
            output = self.transform(content)
            self.save(output)
            if should_cache:
                self.manager.gen.cache.memo_output(rel_path, self.out_path, hashed)

    @abstractmethod
    def initialize(self) -> None:
        pass

    def transform(self, content: str | bytes) -> str | bytes:
        return content

    def save(self, new_content: str | bytes, **kwargs) -> None:
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        kwargs = {
            'mode': 'wb+' if self.byte_mode else 'w+'
        }
        if self.byte_mode is False:
            kwargs['encoding'] = 'utf-8'
        with self.out_path.open(**kwargs) as file:
            file.write(new_content)
