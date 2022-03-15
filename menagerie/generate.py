import sys
from pathlib import Path

from Items.Managers.PageManager import PageManager
from Settings import setup_settings
from menagerie.utils.logger import Logger

__all__ = (
    'main'
)

managers = (PageManager,)


def main(*argv):
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
    Logger.log_info("Settings Up")
    [man.setup() for man in managers]
    Logger.log_info("Beginning Generation")
    # TODO: Progressbar
    Logger.log_info("Finding Content")
    [man.find() for man in managers]
    Logger.log_info("Initializing Meta Data")
    [man.initialize() for man in managers]
    Logger.log_info("Generating Content")
    [man.generate() for man in managers]
    Logger.log_info("Done!")


if __name__ == "__main__":
    main(*sys.argv)
