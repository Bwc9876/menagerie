import argparse
from pathlib import Path

from menagerie.generate import generate
from menagerie.new_project import new_project

__version__ = '0.1.3'


def get_parser():
    # Root Parser
    parser = argparse.ArgumentParser(description="Run a menagerie command")
    parser.add_argument("-v", "--version", action='version', version=__version__)
    subparsers = parser.add_subparsers(title='command', dest='command', required=True)

    # New Project Parser
    new_proj_parser = subparsers.add_parser('new-project', help="Start a new menagerie site")
    new_proj_parser.add_argument('name', help="The new folder to create and place the new project in",
                                 default="NewProject")

    # Generate Parser
    gen_parser = subparsers.add_parser('generate', help="Generate an existing menagerie site")
    gen_parser.add_argument("-c", "--config", help="Specify a different config file to use", default="config.json",
                            type=Path)
    gen_parser.add_argument("--clear-cache", action="store_true", help="Clear the cache before generating")

    return parser


def execute_from_commandline(args: list[str] = None):
    parser = get_parser()
    if args is None:
        parsed_args = parser.parse_args()
    else:
        parsed_args = parser.parse_args(args)
    if parsed_args.command == 'generate':
        generate(Path(parsed_args.config), parsed_args.clear_cache)
    elif parsed_args.command == 'new-project':
        new_project(parsed_args.name)
