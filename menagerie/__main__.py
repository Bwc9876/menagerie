import sys

import menagerie
from . import new_project, generate

if __name__ == '__main__':
    if sys.argv[1] == 'new-project':
        try:
            new_project(sys.argv[2])
        except IndexError:
            new_project("NewProject")
    elif sys.argv[1] == 'generate':
        generate(*sys.argv)
    elif sys.argv[1] == 'version':
        print(f"Menagerie Version: {menagerie.__version__}")
    else:
        print(menagerie.__help__)
