import os
import shutil
import importlib.resources as pkg_resources
import sys
from pathlib import Path

import menagerie


def new_project(name: str):
    with pkg_resources.path(menagerie, 'project_template') as template_path:
        new_path = Path(os.getcwd(), name)
        shutil.copytree(template_path, new_path)
