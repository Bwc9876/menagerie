import sys
from pathlib import Path

from menagerie.Items.Managers.MetaManager import MetaManager
from menagerie.Items.Managers.PageManager import PageManager
from menagerie.Items.Managers.StaticManager import StaticManager
from menagerie.Settings import setup_settings, Settings
from menagerie.SiteGen import SiteGen
from menagerie.utils.logger import Logger

__all__ = (
    'generate',
)


def generate(*argv):
    config_path = None
    for arg in argv:
        if '--config=' in arg:
            try:
                config_path = Path(arg.split('=')[1])
                break
            except IndexError:
                Logger.log_error("Usage: python generate.py --config=CONFIG_PATH")
                return
    if config_path is None:
        config_path = Path('config.json')
    Logger.log_info("Loading Config")
    setup_settings(config_path)
    managers = (PageManager, StaticManager, MetaManager)
    Logger.log_info("Setting Up")
    gen = SiteGen(Settings, managers)
    Logger.log_info("Beginning Generation")
    Logger.log_info("Finding Content")
    gen.find()
    Logger.log_info("Initializing Meta Data")
    gen.initialize()
    Logger.log_info("Generating Content")
    gen.generate()
    Logger.log_info("Done!")


if __name__ == "__main__":
    generate(*sys.argv)
