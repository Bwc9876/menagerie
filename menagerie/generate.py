import sys
from pathlib import Path

from menagerie.Items.Managers.MetaManager import MetaManager
from menagerie.Items.Managers.PageManager import PageManager
from menagerie.Items.Managers.StaticManager import StaticManager
from menagerie.Settings import setup_settings
from menagerie.SiteGen import SiteGen
from menagerie.utils.logger import Logger

__all__ = (
    'generate',
)


def generate(config_path: Path):
    Logger.log_info("Loading Config")
    config = setup_settings(config_path)
    managers = (PageManager, StaticManager, MetaManager)
    Logger.log_info("Setting Up")
    gen = SiteGen(config, managers)
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
