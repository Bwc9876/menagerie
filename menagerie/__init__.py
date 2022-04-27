import sys
import argparse
from pathlib import Path
from textwrap import dedent

from menagerie.generate import generate
from menagerie.new_project import new_project

__version__ = '0.1.1'
__help__ =  dedent("""
                Usage:
                    menagerie new-project [name] : Creates a new menagerie project with a given name
                    menagerie generate [config] : Generates a site with the given config
                    menagerie help : Shows this message
                    menagerie version : Shows the version
            """)

def get_parser():
    
    # Root Parser
    parser = argparse.ArgumentParser(description="Run a menagerie command")
    parser.add_argument("command", choices=['generate', 'new-project'], help="The command you wish to perform")
    parser.add_argument("--version", action='version', version=__version__)
    subparsers = parser.add_subparsers(help='sub-command help')

    # New Project Parser
    new_proj_parser = subparsers.add_parser('new-project', help="new-project help")
    new_proj_parser.add_argument('name', help="The new folder to create and place the new project in", default="NewProject")

    # Generate Parser
    gen_parser = subparsers.add_parser('generate', help="generate help")
    gen_parser.add_argument("--config", help="Specify a differeny config file to use", default="config.json", type=argparse.FileType('r', encoding='utf-8'))

    return parser


def execute_from_commandline(args: list[str] = None):
    parser = get_parser()
    if args is None:
        parsed_args = parser.parse_args()
    else:
        parsed_args = parser.parse_args(args)
    if parsed_args.command == 'generate':
        generate(Path(parsed_args.config))
    elif parsed_args.command == 'new-project':
        new_project(parsed_args.name)
