import sys
from pathlib import Path

import menagerie
from . import new_project, generate

if __name__ == '__main__':
    match [arg.lower() for arg in sys.argv[1:]]:
        case ['new-project']:
            new_project("NewProject")
        case ['new-project', name]:
            new_project(name)
        case ['generate']:
            generate(Path('config.json'))
        case ['generate', Path(config_path)]:
            generate(config_path)
        case ['version']:
            print(f"Menagerie Version: {menagerie.__version__}")
        case ['help']:
            print(menagerie.__help__)
        case _:
            print(f"Invalid Command '{' '.join(sys.argv)}'")
            print(menagerie.__help__)
