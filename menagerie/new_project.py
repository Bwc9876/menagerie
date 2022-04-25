import importlib.resources as pkg_resources
import os
import shutil
from pathlib import Path

import menagerie
from menagerie.utils.logger import Logger


def new_project(name: str):
    with pkg_resources.path(menagerie, 'project_template') as template_path:
        new_path = Path(os.getcwd(), name)
        shutil.copytree(template_path, new_path)
        Logger.log_info(f"New Project '{new_path}' started!")
