from pathlib import Path

from Items.Managers.PageManager import PageManager
from Settings import setup_settings

setup_settings(Path('config.json'))
PageManager.find()
PageManager.initialize()
PageManager.generate()
