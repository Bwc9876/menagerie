from pathlib import Path
from json import load


class Settings:
    pass


def setup_settings(config_path: Path):
    Settings.__dict__ = load(config_path)
