import sys
from pathlib import Path

from Items.Managers.PageManager import PageManager
from Settings import setup_settings
from utils.logger import Logger

managers = (PageManager,)

def main(*argv):
    config_path = None
    for arg in argv:
        if '--config=' in args:
            try:
                config_path = Path(arg.split('=')[1])
                break
            except IndexError:
                print("Usage: python generate.py --config=CONFIG_PATH")
    if config_path is None:
        config_path = Path('config.json')
    Logger.log_info("Loading Config")
    setup_settings(config_path)
    Logger.log_info("Beginning Generation")
    # TODO: Progressbar
    Logger.log_info("Finding Content")
    for man in managers:
        man.find()
    Logger.log_info("Initializing Meta Data")
    for man in managers:
        man.initialize()
    Logger.log_info("Generating Content")
    for man in managers:
        man.generate()
    Logger.log_info("Done!")


if __name__ == "__main__":
    main(*sys.argv)


