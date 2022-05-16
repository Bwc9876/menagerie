import hashlib
from json import loads, dumps
from pathlib import Path
from shutil import rmtree

from menagerie.Items.AbstractItem import AbstractItem

__all__ = ('CacheHandler',)

from menagerie.Settings import Settings


class CacheHandler:
    HASH_ALGORITHM = 'sha256'

    def __init__(self, folder: Path, settings: Settings):
        self.settings = settings
        if self.settings['cache_enabled'] is False:
            return

        self.cache_folder = folder
        self.hash_file = Path(self.cache_folder, "hashes.json")
        self.out_cache = Path(self.cache_folder, "out_cache/")
        self.cache_folder.mkdir(parents=True, exist_ok=True)
        self.out_cache.mkdir(parents=True, exist_ok=True)

        if self.hash_file.exists():
            self.hashes = loads(self.hash_file.read_text(encoding='utf-8'))
        else:
            self.hashes = {'config': "", 'meta': None, 'items': {}}

        config_hash = self.get_hash(settings['config_path'].read_bytes())
        if self.hashes['config'] != config_hash:
            self.invalidate()
            self.hashes['config'] = config_hash

    def invalidate(self):
        rmtree(self.out_cache)
        self.out_cache.mkdir(parents=True, exist_ok=True)
        self.hashes = {'config': "", 'meta': None, 'items': {}}

    def get_hash(self, content: bytes) -> str:
        hasher = hashlib.new(self.HASH_ALGORITHM)
        hasher.update(content)
        return hasher.hexdigest()

    def get_out_cache_path(self, out_path: Path):
        return Path(self.out_cache, out_path.relative_to(self.settings['out_dir']))

    def check_for_hit(self, rel_path: str, content: str) -> [bool, str]:
        hashed_content = self.get_hash(bytes(content, 'utf-8'))
        return (rel_path in self.hashes['items'].keys() and self.hashes['items'][rel_path] == hashed_content), hashed_content

    def get_cached_output(self, out_path: Path) -> str:
        return self.get_out_cache_path(out_path).read_text(encoding='utf-8')

    def check_for_meta_change(self, nav_items: list):
        # If the metadata for any item changes (such as the title), all pages may need to regenerated
        hasher = hashlib.new(self.HASH_ALGORITHM)
        for item in nav_items:
            hasher.update(bytes(dumps(item.as_dict()), 'utf-8'))
        current_hash = hasher.hexdigest()
        if self.hashes['meta'] is None:
            self.hashes['meta'] = current_hash
        elif self.hashes['meta'] != current_hash:
            self.invalidate()
            self.hashes['meta'] = current_hash

    def memo_output(self, rel_path: str, out_path: Path, hashed_content: str):
        self.hashes['items'][rel_path] = hashed_content
        cache_path = self.get_out_cache_path(out_path)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(out_path.read_text(encoding='utf-8'), encoding='utf-8')

    def dump(self):
        self.hash_file.write_text(dumps(self.hashes), encoding='utf-8')

