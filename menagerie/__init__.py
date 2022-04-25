import sys
from pathlib import Path
from textwrap import dedent

from menagerie.generate import generate
from menagerie.new_project import new_project

__version__ = '0.1.0'
__help__ =  dedent("""
                Usage:
                    menagerie new-project [name] : Creates a new menagerie project with a given name
                    menagerie generate [config] : Generates a site with the given config
                    menagerie help : Shows this message
                    menagerie version : Shows the version
            """)


def execute_from_commandline(args: list[str] = None):
    if args is None:
        args = sys.argv
    match [arg.lower() for arg in args[1:]]:
        case ['new-project']:
            new_project("NewProject")
        case ['new-project', name]:
            new_project(name)
        case ['generate']:
            generate(Path('config.json'))
        case ['generate', Path(config_path)]:
            generate(config_path)
        case ['version']:
            print(f"Menagerie Version: {__version__}")
        case ['help']:
            print(__help__)
        case _:
            print(f"Invalid Command '{' '.join(sys.argv)}'")
            print(__help__)
