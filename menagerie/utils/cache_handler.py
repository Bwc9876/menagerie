import hashlib
from json import JSONDecoder, JSONEncoder
from pathlib import Path

from menagerie.Items.AbstractItem import AbstractItem

__all__ = ('CacheHandler',)

from menagerie.Settings import Settings


class CacheHandler:
    HASH_ALGORITHM = 'sha256'

    def __init__(self, folder: Path, settings: Settings):
        self.enabled = settings['cache_enabled']
        self.cache_folder = folder
        self.cache_file = Path(self.cache_folder, "item_cache.json")
        self.decoder = JSONDecoder()
        self.encoder = JSONEncoder()
        self.cache_folder.mkdir(parents=True, exist_ok=True)
        if self.cache_file.exists() is False:
            self.cache_file.write_text("{}", encoding='utf-8')
        self.cache_data = self.decoder.decode(self.cache_file.read_text(encoding='utf-8'))

    def get_hash(self, content: bytes) -> str:
        hasher = hashlib.new(self.HASH_ALGORITHM)
        hasher.update(content)
        return hasher.hexdigest()

    def check_item_changed(self, item: AbstractItem) -> bool:
        if self.enabled is False:
            return True
        cache_key = str(item.in_path)
        hashed = self.get_hash(item.get_path_to_open().read_bytes())
        return self.cache_data.get(cache_key, "") != hashed

    def add_item(self, item: AbstractItem) -> None:
        if self.enabled is False:
            return
        cache_key = str(item.in_path)
        hashed = self.get_hash(item.get_path_to_open().read_bytes())
        self.cache_data[cache_key] = hashed
        self.cache_file.write_text(self.encoder.encode(self.cache_data))
